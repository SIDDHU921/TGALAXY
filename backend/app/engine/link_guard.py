import re
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Any, Optional
from app.models.schemas import ExtractedLinkResult, ExtractedAppResult

class LinkGuardEngine:
    """
    Enterprise Pre-Click Link & Application Payload Inspector.
    Equipped with deep keyword inspection across URLs, paths, subdomains, and queries:
    - Deceptive Authentication & Credential Harvest tokens
    - KYC, PAN, Banking & Account Unlock tokens
    - Fake Gift, Reward & Refund tokens
    - Subdomain Brand Hijacking (e.g. paypal.com.evil-domain.com)
    - Abusive TLDs, IP-based URLs, and Shorteners
    - Direct executable / APK / Script Droppers
    """
    def __init__(self):
        # Known URL shortening services that conceal landing targets
        self.url_shorteners = {
            "bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd",
            "rb.gy", "shorturl.at", "ow.ly", "buff.ly", "goo.gl", "v.gd"
        }
        
        # Abusive Top-Level Domains frequently utilized in phishing campaigns
        self.risky_tlds = {
            "xyz", "top", "work", "click", "buzz", "site", "fun",
            "tk", "ml", "ga", "cf", "gq", "icu", "cam", "rest", "monster",
            "fit", "link", "live", "online", "club", "space", "bid", "download",
            "racing", "kim", "party", "trade", "date", "faith", "cricket"
        }
        
        # Comprehensive Global and Regional Brand Monitored List
        self.official_brand_domains = {
            "paypal": "paypal.com",
            "amazon": "amazon.com",
            "apple": "apple.com",
            "microsoft": "microsoft.com",
            "google": "google.com",
            "netflix": "netflix.com",
            "chase": "chase.com",
            "wellsfargo": "wellsfargo.com",
            "bankofamerica": "bankofamerica.com",
            "citi": "citi.com",
            "capitalone": "capitalone.com",
            "sbi": "onlinesbi.sbi",
            "hdfc": "hdfcbank.com",
            "icici": "icicibank.com",
            "axis": "axisbank.com",
            "paytm": "paytm.com",
            "phonepe": "phonepe.com",
            "usps": "usps.com",
            "fedex": "fedex.com",
            "dhl": "dhl.com",
            "ups": "ups.com",
            "indiapost": "indiapost.gov.in",
            "binance": "binance.com",
            "coinbase": "coinbase.com",
            "metamask": "metamask.io",
            "safari": "apple.com",
            "chrome": "google.com",
            "android": "android.com",
            "windows": "microsoft.com",
            "whatsapp": "whatsapp.com",
            "facebook": "facebook.com",
            "instagram": "instagram.com",
            "telegram": "telegram.org"
        }
        
        # Fraud and Phishing Keywords Monitored within URL Subdomains, Paths, and Parameters
        self.url_fraud_keywords = {
            "CREDENTIAL_ACCESS": {
                "label": "Credential & Login Harvesting Token",
                "weight": 35,
                "tokens": ["login", "signin", "sign-in", "log-in", "auth", "authenticate", "sso", "portal", "webscr", "secure-login", "verify-login", "session"]
            },
            "ACCOUNT_COMPLIANCE": {
                "label": "Account Update / KYC Token",
                "weight": 35,
                "tokens": ["verify", "verification", "update", "account-update", "validate", "confirm", "kyc", "pan", "pan-update", "aadhaar", "re-kyc", "security-check", "unlock", "restore"]
            },
            "FINANCIAL_DECEPTION": {
                "label": "Banking / Wallet / Crypto Token",
                "weight": 30,
                "tokens": ["netbanking", "ebanking", "onlinebanking", "wallet", "wallet-connect", "web3", "airdrop", "seed-phrase", "binance-verify", "metamask-auth", "tax-refund", "refund", "money", "cash", "dollar", "payout"]
            },
            "LURE_OFFER": {
                "label": "Prize / Reward / Lottery Lure Token",
                "weight": 35,
                "tokens": [
                    "win", "winner", "winning", "prize", "prizepool", "prizes", "jackpot", "grandprize",
                    "gift", "giftcard", "free-gift", "reward", "rewards-point", "claim-reward", "claim",
                    "redeem", "bonus", "lucky-draw", "spin", "cashback", "win-cash", "giveaway", "freebie"
                ]
            },
            "DELIVERY_SCAM": {
                "label": "Delivery Tracking Lure Token",
                "weight": 30,
                "tokens": ["usps-track", "dhl-parcel", "fedex-delivery", "redelivery", "customs-fee", "parcel-hold", "shipping-update"]
            },
            "MALICIOUS_DOWNLOAD": {
                "label": "Executable / Dropper Token",
                "weight": 40,
                "tokens": ["download", "installer", "setup", "update-patch", "app-download", "apk-download", "patch-update", "security-apk"]
            }
        }
        
        # Dangerous executable / application extensions
        self.dangerous_extensions = {
            ".apk": ("Android Package (APK)", "High danger: can install malicious trojans, spyware, or keyloggers outside the app store"),
            ".exe": ("Windows Executable", "Critical danger: can execute arbitrary binary code on your device"),
            ".scr": ("Screen Saver Executable", "High danger: frequently used in ransomware campaigns"),
            ".bat": ("Batch Script", "High danger: can execute command line operations"),
            ".cmd": ("Windows Command Script", "High danger: unauthorized system commands"),
            ".vbs": ("VBScript File", "High danger: scripts that download trojans"),
            ".js": ("JavaScript File", "High danger: payload dropper script"),
            ".iso": ("Disk Image", "Medium danger: used to bypass Windows Mark of the Web checks"),
            ".zip": ("Compressed Archive", "Medium danger: may contain concealed executables")
        }

    def extract_urls(self, text: str) -> List[str]:
        """Extract all URLs or domain strings from raw text."""
        url_pattern = r"(?:https?://|www\.)[^\s<>'\"()]+|\b[a-zA-Z0-9.-]+\.(?:com|org|net|xyz|top|site|info|online|link|click|app|io|biz|ru|cn|buzz|club|fun)(?:/[^\s<>'\"()]*)?"
        found = re.findall(url_pattern, text, re.IGNORECASE)
        deduped = []
        for u in found:
            cleaned = u.rstrip(".,;:!?)'\"")
            if cleaned and cleaned not in deduped:
                deduped.append(cleaned)
        return deduped

    def inspect_url(self, raw_url: str) -> ExtractedLinkResult:
        """
        Deep pre-click analysis of an extracted URL with full token & keyword awareness.
        """
        normalized = raw_url
        if not re.match(r"^https?://", normalized, re.IGNORECASE):
            normalized = "http://" + normalized

        parsed = urlparse(normalized)
        domain = parsed.netloc.lower() or parsed.path.split("/")[0].lower()
        domain = domain.split(":")[0]  # strip port
        full_path_query = (parsed.path + "?" + parsed.query).lower()

        reasons: List[str] = []
        risk_score = 0
        safe_advice = None
        detected_keywords = []

        # 1. Check for raw numeric IP address in host
        is_ip = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain))
        if is_ip:
            risk_score += 45
            reasons.append("Raw numeric IP address used instead of a verified domain name")
            safe_advice = "Legitimate services never ask you to access banking, email, or accounts through raw numeric IP links."

        # 2. Check for URL Shorteners
        for shortener in self.url_shorteners:
            if domain == shortener or domain.endswith("." + shortener):
                risk_score += 25
                reasons.append(f"URL shortener ({shortener}) used to conceal the actual destination")
                safe_advice = "The link destination is hidden behind a redirect shortener. Avoid opening unknown shortened links."

        # 3. Check for Risky / Low-Reputation TLDs
        tld = domain.split(".")[-1] if "." in domain else ""
        if tld in self.risky_tlds:
            risk_score += 35
            reasons.append(f"High-risk Top-Level Domain (.{tld}) commonly used for transient phishing infrastructure")
            safe_advice = f"Domain uses .{tld}, a known high-risk TLD. Verify the sender before visiting."

        # 4. Check for Subdomain Brand Spoofing (e.g. paypal.com.attacker.xyz)
        for brand, official in self.official_brand_domains.items():
            # Check if official domain is used as a fake subdomain prefix on another root domain
            if (f"{brand}.com." in domain or f"{brand}." in domain) and not (domain == official or domain.endswith("." + official)):
                risk_score += 70
                reasons.append(f"Subdomain brand hijacking: mimics '{brand}' inside unverified external domain ({domain})")
                safe_advice = f"🚨 Phishing Alert: The link uses '{brand}' in a subdomain to trick you. The actual host is {domain}."
                break

        # 5. Check for Typosquatting / Homoglyph / Leetspeak Brand Lookalike Deception
        if risk_score < 70:
            for brand, official in self.official_brand_domains.items():
                if brand in domain and not (domain == official or domain.endswith("." + official)):
                    risk_score += 55
                    reasons.append(f"Domain spoofing: contains brand '{brand.title()}' but is NOT the official domain ({official})")
                    safe_advice = f"🚨 Deceptive lookalike! This link is NOT from official {brand.title()} ({official}). Do not enter login details."
                    break

            leetspeak_variants = {
                "paypa1": "PayPal", "amaz0n": "Amazon", "appl3": "Apple",
                "micros0ft": "Microsoft", "g00gle": "Google", "netfl1x": "Netflix",
                "b1nance": "Binance", "sb1": "SBI"
            }
            for variant, brand_name in leetspeak_variants.items():
                if variant in domain:
                    risk_score += 65
                    reasons.append(f"Homoglyph/Leetspeak attack: '{variant}' mimics trusted brand '{brand_name}'")
                    safe_advice = f"🚨 Dangerous deceptive domain mimicking {brand_name}. Visiting may compromise your accounts."
                    break

        # 6. Deep Inspection of Scam/Fraud Keywords in URL Path & Subdomains
        for cat_key, cat_data in self.url_fraud_keywords.items():
            matched_tokens = []
            for token in cat_data["tokens"]:
                # Check if token exists in domain, path, or query
                if token in domain or token in full_path_query:
                    matched_tokens.append(token)
                    if token not in detected_keywords:
                        detected_keywords.append(token)

            if matched_tokens:
                token_weight = min(cat_data["weight"], 40)
                risk_score += token_weight
                reasons.append(f"{cat_data['label']}: detected suspicious keyword '{', '.join(matched_tokens)}' in link path/domain")

        # 7. Check if URL directly points to an executable or dangerous application
        path_lower = parsed.path.lower()
        for ext, (app_name, danger_desc) in self.dangerous_extensions.items():
            if path_lower.endswith(ext):
                risk_score += 60
                reasons.append(f"Direct download link to dangerous payload: {app_name} ({ext})")
                safe_advice = f"🚨 WARNING: This link downloads a {app_name} directly to your device. {danger_desc}."
                break

        # Check for multiple subdomains (entropy / subdomain evasion)
        subdomain_count = domain.count(".")
        if subdomain_count >= 3:
            risk_score += 25
            reasons.append(f"Excessive subdomain nesting ({subdomain_count} dots) used to disguise destination")

        # Check for multiple lure tokens combined
        if len(detected_keywords) >= 2:
            risk_score += 45
            reasons.append(f"Compound lure attack: multiple deceptive keyword tokens detected ({', '.join(detected_keywords[:4])})")

        normalized_score = min(risk_score, 100)
        is_suspicious = normalized_score >= 35

        if not safe_advice:
            if is_suspicious:
                safe_advice = f"Proceed with caution. The security layer detected anomalous domain & link tokens: {', '.join(detected_keywords[:3]) if detected_keywords else 'High-risk characteristics'}."
            else:
                safe_advice = "No anomalous domain signatures or deceptive tokens detected. Standard browsing safe."

        return ExtractedLinkResult(
            original_url=raw_url,
            normalized_url=normalized,
            domain=domain,
            is_suspicious=is_suspicious,
            risk_score=normalized_score,
            threat_reasons=reasons,
            safe_destination_advice=safe_advice
        )

    def extract_and_inspect_apps(self, text: str) -> List[ExtractedAppResult]:
        """Scans message content for mentions of application attachments, APK downloads, or script payloads."""
        results: List[ExtractedAppResult] = []
        file_pattern = r"\b([a-zA-Z0-9_\-\.]+\.(?:apk|exe|scr|bat|cmd|vbs|js|iso|zip|dmg))\b"
        matches = re.finditer(file_pattern, text, re.IGNORECASE)
        seen_files = set()

        for m in matches:
            filename = m.group(1)
            if filename.lower() in seen_files:
                continue
            seen_files.add(filename.lower())
            
            ext = "." + filename.split(".")[-1].lower()
            if ext in self.dangerous_extensions:
                app_name, danger_desc = self.dangerous_extensions[ext]
                risk = 85 if ext in [".apk", ".exe", ".scr", ".bat"] else 60
                results.append(ExtractedAppResult(
                    filename=filename,
                    extension=ext,
                    is_executable=True,
                    risk_score=risk,
                    risk_type=app_name,
                    description=danger_desc
                ))

        return results

    def get_link_keywords_catalog(self) -> List[Dict[str, Any]]:
        """Returns the full catalog of monitored URL tokens and categories for UI display."""
        catalog = []
        for cat_key, data in self.url_fraud_keywords.items():
            catalog.append({
                "category": cat_key,
                "label": data["label"],
                "tokens": data["tokens"]
            })
        return catalog
