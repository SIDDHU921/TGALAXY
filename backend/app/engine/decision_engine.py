import uuid
from datetime import datetime
from typing import Dict, List, Any
from app.engine.trust_graph import TrustGraphEngine
from app.engine.content_nlp import ContentNLPEngine
from app.engine.link_guard import LinkGuardEngine
from app.models.schemas import (
    MessageCheckRequest,
    SecurityAssessment,
    ThreatIndicator,
    ExtractedLinkResult,
    ExtractedAppResult
)

class SecurityDecisionEngine:
    """
    Core pre-interaction decision and policy enforcement layer.
    Combines Sender Trust, Content NLP, Pre-Click Link Forensics, and Application Payloads.
    """
    def __init__(self, trust_graph: TrustGraphEngine, nlp_engine: ContentNLPEngine, link_guard: LinkGuardEngine):
        self.trust_graph = trust_graph
        self.nlp = nlp_engine
        self.link_guard = link_guard

    def assess_message(self, request: MessageCheckRequest) -> SecurityAssessment:
        indicators: List[ThreatIndicator] = []
        layer_scores: Dict[str, int] = {}

        # 1. LAYER 1: SENDER & TRUST GRAPH ANALYSIS
        is_known, contact = self.trust_graph.is_known_contact(request.sender)
        is_impersonating, spoofed_brand, imp_desc = self.trust_graph.detect_impersonation(
            request.sender, request.sender_name, request.content
        )

        sender_risk = 0
        if is_known:
            sender_risk = 0
            indicators.append(ThreatIndicator(
                layer="CONTACT_SENDER",
                severity="LOW",
                code="KNOWN_TRUSTED_CONTACT",
                description=f"Verified saved contact: {contact.name} ({contact.relationship})",
                detail=f"Trust level: {contact.trust_level}. Baseline alerts suppressed to avoid false interruptions."
            ))
        else:
            # Unknown sender baseline scrutiny
            sender_risk = 25
            indicators.append(ThreatIndicator(
                layer="CONTACT_SENDER",
                severity="MEDIUM",
                code="UNKNOWN_EXTERNAL_SENDER",
                description="Sender is not in your saved contacts address book.",
                detail=f"Identifier: {request.sender}. Deep scrutiny mode enabled."
            ))

            if is_impersonating:
                sender_risk = 85
                indicators.append(ThreatIndicator(
                    layer="CONTACT_SENDER",
                    severity="CRITICAL",
                    code="BRAND_IMPERSONATION",
                    description=f"Impersonation Alert: Claims to be {spoofed_brand}",
                    detail=imp_desc
                ))

        layer_scores["sender_risk"] = sender_risk

        # 2. LAYER 2: CONTENT & SEMANTIC NLP ANALYSIS
        nlp_res = self.nlp.analyze(request.content)
        content_risk = nlp_res["nlp_score"]
        layer_scores["content_risk"] = content_risk

        for cat in nlp_res["matched_categories"]:
            sev = "HIGH" if cat["weight"] >= 45 else ("MEDIUM" if cat["weight"] >= 35 else "LOW")
            indicators.append(ThreatIndicator(
                layer="NLP_CONTENT",
                severity=sev,
                code=cat["category"],
                description=cat["label"],
                detail=f"Matched social engineering patterns in text body (Weight: {cat['weight']})"
            ))

        # 3. LAYER 3: PRE-CLICK LINK FORENSICS
        extracted_urls = self.link_guard.extract_urls(request.content)
        inspected_links: List[ExtractedLinkResult] = []
        max_link_risk = 0

        for url in extracted_urls:
            link_res = self.link_guard.inspect_url(url)
            inspected_links.append(link_res)
            if link_res.risk_score > max_link_risk:
                max_link_risk = link_res.risk_score

            if link_res.is_suspicious:
                indicators.append(ThreatIndicator(
                    layer="LINK_PAYLOAD",
                    severity="CRITICAL" if link_res.risk_score >= 60 else "HIGH",
                    code="SUSPICIOUS_LINK_TARGET",
                    description=f"Pre-Click Alert: High-risk URL ({link_res.domain})",
                    detail="; ".join(link_res.threat_reasons)
                ))

        layer_scores["link_risk"] = max_link_risk

        # 4. LAYER 4: APPLICATION & PAYLOAD SCANNER
        extracted_apps = self.link_guard.extract_and_inspect_apps(request.content)
        max_app_risk = 0
        for app in extracted_apps:
            if app.risk_score > max_app_risk:
                max_app_risk = app.risk_score
            indicators.append(ThreatIndicator(
                layer="APP_PAYLOAD",
                severity="CRITICAL" if app.risk_score >= 80 else "HIGH",
                code="DANGEROUS_APP_PAYLOAD",
                description=f"Suspicious App Payload: {app.filename}",
                detail=f"{app.risk_type}: {app.description}"
            ))

        layer_scores["app_risk"] = max_app_risk

        # 5. OVERALL COMPOSITE RISK CALCULATION
        if is_known:
            # If known contact, only escalate if high-risk link or app is present (compromised account)
            if max_link_risk >= 60 or max_app_risk >= 60:
                overall_score = max(max_link_risk, max_app_risk)
                indicators.append(ThreatIndicator(
                    layer="CONTACT_SENDER",
                    severity="HIGH",
                    code="POTENTIAL_ACCOUNT_TAKEOVER",
                    description="Known contact sending uncharacteristically high-risk link or payload",
                    detail="The sender's account may be compromised or forwarding automated spam."
                ))
            else:
                # Benign interaction from trusted contact
                overall_score = min(content_risk // 4, 15)
        else:
            # Unknown sender calculation
            # Extreme threat: Malicious APK/payload or Brand Impersonation
            if is_impersonating or max_app_risk >= 60:
                overall_score = max(sender_risk, max_app_risk, 85)
            # High-risk phishing/malicious link (link_risk >= 60)
            elif max_link_risk >= 60:
                overall_score = min(max_link_risk + 15 + (content_risk // 4), 100)
            # Compound smishing attacks: Unknown sender + (Fraud/Offer NLP OR Urgency) + Suspicious Link
            elif content_risk >= 35 and max_link_risk >= 25:
                overall_score = min(75 + (content_risk // 4) + (max_link_risk // 4), 95)
            # Suspicious link or dangerous file alone from unknown sender
            elif max_link_risk >= 35 or max_app_risk >= 45:
                overall_score = max(max_link_risk, max_app_risk) + 15
            # Suspicious content alone from unknown sender
            elif content_risk >= 35:
                overall_score = min(content_risk + 15, 70)
            else:
                # Completely ordinary message from unknown sender (e.g. 'Hello, are you there?')
                overall_score = 20

        # 6. DISPOSITION & PRE-INTERACTION ACTIONS
        if overall_score >= 75:
            disposition = "BLOCK"
            action_banner = "🛡️ PRE-INTERACTION DEFENSE: High Threat Blocked"
            summary = "Dangerous message intercepted before user interaction. High probability of fraud, phishing, or malicious application."
            recommendation = "Do not open, click links, or download attached applications. Threat has been quarantined."
        elif overall_score >= 35:
            disposition = "WARN"
            action_banner = "⚠️ PRE-INTERACTION ADVISORY: Suspicious Activity Detected"
            summary = "Suspicious message from unverified source. Contains promotional cues, urgency, or unverified links."
            recommendation = "Exercise caution before clicking links or replying. Verify sender identity through an alternate trusted channel."
        else:
            disposition = "SAFE"
            action_banner = "✅ VERIFIED SAFE: Communication Clear"
            summary = "Message evaluated as legitimate. No malicious links, apps, or deceptive tactics identified."
            recommendation = "Safe to read and interact normally."

        return SecurityAssessment(
            id=f"sec-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sender=request.sender,
            sender_name=request.sender_name,
            channel=request.channel,
            is_known_contact=is_known,
            overall_score=overall_score,
            disposition=disposition,
            action_banner=action_banner,
            summary=summary,
            recommendation=recommendation,
            indicators=indicators,
            extracted_links=inspected_links,
            extracted_apps=extracted_apps,
            layer_scores=layer_scores
        )
