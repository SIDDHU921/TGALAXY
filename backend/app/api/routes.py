from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.schemas import (
    MessageCheckRequest,
    LinkCheckRequest,
    SecurityAssessment,
    ExtractedLinkResult,
    Contact,
    ContactCreate,
    TelemetryStats,
    Scenario
)
from app.engine.trust_graph import TrustGraphEngine
from app.engine.content_nlp import ContentNLPEngine
from app.engine.link_guard import LinkGuardEngine
from app.engine.decision_engine import SecurityDecisionEngine
from app.engine.url_keyword_deep_analyzer import DeepLinkKeywordAnalyzer
from app.samples.scenarios import get_all_scenarios

router = APIRouter()

# Singletons for service state
trust_graph = TrustGraphEngine()
nlp_engine = ContentNLPEngine()
link_guard = LinkGuardEngine()
decision_engine = SecurityDecisionEngine(trust_graph, nlp_engine, link_guard)
deep_link_analyzer = DeepLinkKeywordAnalyzer()

# In-memory telemetry and threat audit log
telemetry_data = {
    "total_inspected": 0,
    "safe_count": 0,
    "warn_count": 0,
    "blocked_count": 0,
    "malicious_links_caught": 0,
    "dangerous_apps_stopped": 0,
    "fake_offers_intercepted": 0,
    "impersonations_detected": 0
}

threat_history: List[SecurityAssessment] = []

@router.post("/check-message", response_model=SecurityAssessment)
def check_message(req: MessageCheckRequest):
    """
    Main pre-interaction security gateway endpoint.
    Intercepts and inspects sender identity, message NLP, links, and payloads.
    """
    assessment = decision_engine.assess_message(req)
    
    # Update telemetry counters
    telemetry_data["total_inspected"] += 1
    if assessment.disposition == "SAFE":
        telemetry_data["safe_count"] += 1
    elif assessment.disposition == "WARN":
        telemetry_data["warn_count"] += 1
    elif assessment.disposition == "BLOCK":
        telemetry_data["blocked_count"] += 1

    # Update granular threat metric counters
    for ind in assessment.indicators:
        if ind.code == "SUSPICIOUS_LINK_TARGET":
            telemetry_data["malicious_links_caught"] += 1
        elif ind.code == "DANGEROUS_APP_PAYLOAD":
            telemetry_data["dangerous_apps_stopped"] += 1
        elif ind.code == "FAKE_OFFER_LOTTERY":
            telemetry_data["fake_offers_intercepted"] += 1
        elif ind.code == "BRAND_IMPERSONATION":
            telemetry_data["impersonations_detected"] += 1

    # Keep latest 50 in history
    threat_history.insert(0, assessment)
    if len(threat_history) > 50:
        threat_history.pop()

    return assessment

@router.post("/check-link", response_model=ExtractedLinkResult)
def check_link(req: LinkCheckRequest):
    """
    Standalone pre-click link forensics endpoint.
    Inspects URL before user navigation.
    """
    return link_guard.inspect_url(req.url)

@router.post("/deep-link-analysis")
def deep_link_analysis(req: LinkCheckRequest):
    """
    Forensic deep dissection of any link, analyzing every single keyword
    across scheme, subdomains, host, path segments, and query parameters.
    """
    return deep_link_analyzer.dissect_url(req.url)

@router.get("/scenarios", response_model=List[Scenario])
def list_scenarios():
    """Retrieve pre-configured real-world attack and legitimate scenarios for testing."""
    return get_all_scenarios()

@router.get("/contacts", response_model=List[Contact])
def list_contacts():
    """Retrieve list of saved trusted contacts in address book."""
    return trust_graph.get_all_contacts()

@router.post("/contacts", response_model=Contact)
def add_contact(req: ContactCreate):
    """Add a new contact to the address book trust graph."""
    return trust_graph.add_contact(req)

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    """Remove a contact from the address book."""
    success = trust_graph.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"status": "success", "message": f"Contact {contact_id} removed"}

@router.get("/telemetry", response_model=TelemetryStats)
def get_telemetry():
    """Get real-time security telemetry and threat statistics."""
    return TelemetryStats(**telemetry_data)

@router.get("/threat-history", response_model=List[SecurityAssessment])
def get_history():
    """Get the recent inspection history audit trail."""
    return threat_history

@router.get("/threat-lexicon")
def get_threat_lexicon():
    """Get the full catalog of monitored fraud categories, keywords, and link tokens."""
    return {
        "nlp_categories": nlp_engine.get_lexicon_catalog(),
        "url_categories": link_guard.get_link_keywords_catalog(),
        "risky_tlds": list(link_guard.risky_tlds),
        "monitored_brands": list(link_guard.official_brand_domains.keys())
    }

@router.post("/reset-telemetry")
def reset_telemetry():
    """Reset telemetry metrics for fresh demonstration."""
    for k in telemetry_data:
        telemetry_data[k] = 0
    threat_history.clear()
    return {"status": "success", "message": "Telemetry reset successfully"}
