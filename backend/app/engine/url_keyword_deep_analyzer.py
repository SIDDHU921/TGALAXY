import re
import math
import collections
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Optional


class DeepLinkKeywordAnalyzer:
    """
    Exhaustive Forensic URL & Link Keyword Analyzer.
    Deconstructs URLs into anatomical components (Scheme, Subdomains, Host, TLD, Path, Query, Fragment)
    and evaluates every token against 200+ specialized fraud & phishing keywords.
    """
    def __init__(self):
        # 12 Exhaustive Link Scam Keyword Classes
        self.keyword_categories = {
            "AUTHENTICATION_HARVEST": {
                "label": "Credential & Login Harvesting",
                "severity": "CRITICAL",
                "base_weight": 35,
                "description": "Tokens designed to mimic legitimate login screens and capture usernames and passwords.",
                "tokens": [
                    "login", "signin", "sign-in", "log-in", "auth", "authenticate", "sso", "portal",
                    "webscr", "secure-login", "verify-login", "session", "credential", "account-access",
                    "identity-check", "oauth", "password", "passcode", "security-login", "member-login"
                ]
            },
            "SECURITY_COMPLIANCE": {
                "label": "Security & Account Recovery Deception",
                "severity": "HIGH",
                "base_weight": 30,
                "description": "Tokens falsely claiming security checks, account reactivations, or unblocking procedures.",
                "tokens": [
                    "verify", "verification", "security-check", "security-update", "update", "validate",
                    "confirm", "restore", "reactivate", "unlock", "unfreeze", "re-verify", "compliance",
                    "account-recovery", "resolve", "appeal", "resolution-center", "remedy"
                ]
            },
            "KYC_BANKING_FINANCE": {
                "label": "KYC, PAN & NetBanking Exploitation",
                "severity": "CRITICAL",
                "base_weight": 40,
                "description": "Tokens targeting identity documents (KYC, PAN, Aadhaar) and core netbanking credentials.",
                "tokens": [
                    "kyc", "re-kyc", "e-kyc", "kyc-update", "pan", "pan-card", "pan-update", "aadhaar",
                    "netbanking", "ebanking", "onlinebanking", "banking", "bank-login", "cibil",
                    "debit-card", "credit-card", "cvv", "card-activation", "pin-reset", "account-number"
                ]
            },
            "CRYPTO_WEB3_DRAIN": {
                "label": "Crypto Wallet & Web3 Drainer",
                "severity": "CRITICAL",
                "base_weight": 40,
                "description": "Tokens designed to connect Web3 wallets, drain funds, or phish 12-word seed phrases.",
                "tokens": [
                    "wallet", "wallet-connect", "connect-wallet", "web3", "airdrop", "claim-airdrop",
                    "seed-phrase", "recovery-phrase", "private-key", "metamask", "trustwallet",
                    "binance-verify", "coinbase-auth", "uniswap-claim", "presale", "token-claim"
                ]
            },
            "BILLING_UTILITY_DISCONNECTION": {
                "label": "Billing, Tax & Utility Extortion",
                "severity": "HIGH",
                "base_weight": 35,
                "description": "Tokens associated with fake electricity bills, unpaid utility debts, or bogus tax refunds.",
                "tokens": [
                    "bill", "pay-bill", "billing", "invoice", "receipt", "refund", "tax-refund", "rebate",
                    "chargeback", "electricity", "light-bill", "power-bill", "gas-bill", "disconnection",
                    "due-payment", "overdue", "bill-desk", "utility-pay"
                ]
            },
            "LURE_LOTTERY_REWARD": {
                "label": "Prize, Lottery & Free Lure Tokens",
                "severity": "HIGH",
                "base_weight": 35,
                "description": "Tokens offering fake prizes, gift cards, bonus cash, or expired credit card points.",
                "tokens": [
                    "win", "winner", "winning", "prize", "prizepool", "prizes", "jackpot", "grandprize",
                    "gift", "giftcard", "free-gift", "reward", "rewards", "rewards-point", "claim-reward",
                    "claim-prize", "claim", "redeem", "lucky-draw", "luckydraw", "bonus", "cashback",
                    "voucher", "spin-win", "spin", "free-iphone", "win-cash", "money", "cash", "dollar",
                    "payout", "giveaway", "lottery", "contest-winner", "freebie"
                ]
            },
            "DELIVERY_SMISHING": {
                "label": "Package Delivery & Customs Phishing",
                "severity": "HIGH",
                "base_weight": 35,
                "description": "Tokens imitating postal couriers, redelivery fees, or customs clearance payments.",
                "tokens": [
                    "tracking", "track", "usps-track", "dhl-parcel", "fedex-delivery", "ups-tracking",
                    "redelivery", "customs", "customs-fee", "parcel-hold", "shipping-update",
                    "delivery-notice", "reschedule", "address-confirm"
                ]
            },
            "JOB_TASK_FRAUD": {
                "label": "Job, Task & Commission Scheme Tokens",
                "severity": "MEDIUM",
                "base_weight": 30,
                "description": "Tokens promising daily income for completing tasks, liking videos, or joining Telegram channels.",
                "tokens": [
                    "job", "part-time", "task", "task-portal", "youtube-task", "earn-daily", "telegram-task",
                    "daily-payout", "commission", "vip-group", "work-from-home", "salary-claim"
                ]
            },
            "MALWARE_PAYLOAD_DROPPER": {
                "label": "Malware, APK & Executable Dropper",
                "severity": "CRITICAL",
                "base_weight": 50,
                "description": "Tokens directly initiating unverified executable or APK downloads outside trusted app stores.",
                "tokens": [
                    "download", "installer", "setup", "update-patch", "app-download", "apk-download",
                    "security-patch", "patch-update", "client.apk", "mod.apk", "security-apk", "payload"
                ]
            },
            "TELECOM_SIM_DEACTIVATION": {
                "label": "SIM Card & Telecom Deactivation",
                "severity": "HIGH",
                "base_weight": 35,
                "description": "Tokens threatening SIM deactivation or pushing unverified eSIM/5G update forms.",
                "tokens": [
                    "sim", "esim", "sim-upgrade", "trai", "5g-upgrade", "port-sim", "sim-verification",
                    "deactivation", "telecom-notice", "sim-swap", "keep-active"
                ]
            },
            "URGENCY_PRESSURE": {
                "label": "Urgency & Expiration Coercion",
                "severity": "MEDIUM",
                "base_weight": 25,
                "description": "Tokens injecting artificial time pressure into the link destination.",
                "tokens": [
                    "urgent", "immediate", "expire", "expiring-today", "24h", "final-notice", "warning",
                    "action-required", "urgent-notice", "last-chance", "deadline"
                ]
            },
            "EVASION_REDIRECT": {
                "label": "Evasion & Traffic Redirection",
                "severity": "MEDIUM",
                "base_weight": 25,
                "description": "Tokens used to daisy-chain redirects and evade security web-crawlers.",
                "tokens": [
                    "redirect", "goto", "out", "link-relay", "url-forward", "jump", "tracker",
                    "click-track", "bounce", "relay", "r.php", "go.php"
                ]
            }
        }

        # Monitored Brands for Subdomain & Typosquatting Checks (including tech ecosystems)
        self.monitored_brands = {
            "paypal": "paypal.com",
            "amazon": "amazon.com",
            "apple": "apple.com",
            "microsoft": "microsoft.com",
            "google": "google.com",
            "netflix": "netflix.com",
            "safari": "apple.com",
            "chrome": "google.com",
            "android": "android.com",
            "windows": "microsoft.com",
            "chase": "chase.com",
            "wellsfargo": "wellsfargo.com",
            "bankofamerica": "bankofamerica.com",
            "citi": "citi.com",
            "capitalone": "capitalone.com",
            "sbi": "onlinesbi.sbi",
            "hdfc": "hdfcbank.com",
            "icici": "icicibank.com",
            "axis": "axisbank.com",
            "pnb": "pnbindia.in",
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
            "whatsapp": "whatsapp.com",
            "telegram": "telegram.org",
            "facebook": "facebook.com",
            "instagram": "instagram.com"
        }

        # Verified Trusted Domains — never flag these regardless of path/query tokens
        self.trusted_domains = {
            "google.com", "microsoft.com", "login.microsoft.com", "apple.com",
            "amazon.com", "facebook.com", "instagram.com", "twitter.com",
            "linkedin.com", "github.com", "youtube.com", "wikipedia.org",
            "paypal.com", "netflix.com", "spotify.com", "adobe.com",
            "live.com", "outlook.com", "office.com", "onedrive.com",
            "accounts.google.com", "login.live.com", "auth0.com",
            "okta.com", "zoom.us", "dropbox.com", "box.com",
            "cloudflare.com", "aws.amazon.com", "console.aws.amazon.com",
            "portal.azure.com", "store.steampowered.com",
        }

        # High-Risk Disposable TLDs
        self.abusive_tlds = {
            "xyz", "top", "work", "click", "buzz", "site", "fun",
            "tk", "ml", "ga", "cf", "gq", "icu", "cam", "rest", "monster",
            "fit", "link", "live", "online", "club", "space", "bid", "download",
            "racing", "kim", "party", "trade", "date", "faith", "cricket"
        }

    def _shannon_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of a string (higher = more random/gibberish)."""
        if not text:
            return 0.0
        freq = collections.Counter(text)
        length = len(text)
        return -sum((c / length) * math.log2(c / length) for c in freq.values())

    def _is_gibberish(self, word: str) -> bool:
        """
        Detect if a word looks randomly generated (gibberish domain).
        Checks: high consonant cluster ratio, no vowel pattern, high char entropy.
        """
        if len(word) < 6:
            return False
        vowels = set("aeiou")
        consonants = set("bcdfghjklmnpqrstvwxyz")
        word_l = word.lower()
        # Count vowel/consonant ratio
        vowel_count = sum(1 for c in word_l if c in vowels)
        consonant_count = sum(1 for c in word_l if c in consonants)
        total_alpha = vowel_count + consonant_count
        if total_alpha == 0:
            return False
        vowel_ratio = vowel_count / total_alpha
        # Find max consecutive consonant run
        max_consonant_run = 0
        current_run = 0
        for c in word_l:
            if c in consonants:
                current_run += 1
                max_consonant_run = max(max_consonant_run, current_run)
            else:
                current_run = 0
        entropy = self._shannon_entropy(word_l)
        # Gibberish signals:
        # 1. Very few vowels (< 20% of alpha chars)
        # 2. High consonant run (>= 4 consecutive consonants)
        # 3. High char entropy (>= 3.5 bits) for short words
        signals = 0
        if vowel_ratio < 0.20:
            signals += 1
        if max_consonant_run >= 4:
            signals += 1
        if entropy >= 3.5 and len(word_l) <= 12:
            signals += 1
        if len(word_l) >= 8 and vowel_ratio < 0.25 and entropy >= 3.2:
            signals += 1
        return signals >= 2

    def dissect_url(self, raw_url: str) -> Dict[str, Any]:
        """
        Performs a full forensic dissection of a URL, analyzing every keyword token in every segment.
        """

        normalized = raw_url.strip()
        if not re.match(r"^https?://", normalized, re.IGNORECASE):
            normalized = "http://" + normalized

        parsed = urlparse(normalized)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Fast-path: trusted verified domain check (HTTPS required)
        _host_check = netloc.split("@")[-1].split(":")[0]
        _is_trusted = scheme == "https" and (
            _host_check in self.trusted_domains or
            any(_host_check == td or _host_check.endswith("." + td)
                for td in self.trusted_domains)
        )
        if _is_trusted:
            return {
                "original_url": raw_url, "normalized_url": normalized,
                "anatomy": {"scheme": scheme, "host": _host_check,
                            "subdomains": [], "domain": "", "tld": "",
                            "port": None, "path": parsed.path.lower(),
                            "path_segments": [], "query_params": {},
                            "fragment": "", "is_ip_host": False,
                            "is_abusive_tld": False, "has_auth_abuse": False,
                            "payload_extension": None},
                "flagged_keywords": [], "total_keywords_detected": 0,
                "threat_reasons": ["Verified trusted domain — pre-interaction safe."],
                "composite_risk_score": 0, "verdict": "SAFE",
                "verdict_badge": "✅ BENIGN / SAFE LINK",
                "safe_advice": "This domain is a verified trusted provider. No threat indicators found.",
                "risk_score": 0,
            }
        
        # Check for HTTP basic auth injection (@ symbol abuse: e.g. https://google.com@evil.com)
        has_auth_abuse = "@" in netloc
        host = netloc.split("@")[-1] if has_auth_abuse else netloc
        
        # Extract port if present
        port = None
        if ":" in host:
            host_parts = host.split(":")
            host = host_parts[0]
            port = host_parts[1]

        # Decompose Hostname into Subdomains, Second-Level Domain (SLD), and TLD
        host_parts = host.split(".")
        tld = host_parts[-1] if len(host_parts) > 1 else ""
        domain = host_parts[-2] if len(host_parts) > 1 else host
        subdomains = host_parts[:-2] if len(host_parts) > 2 else []

        # Parse Path Segments
        path = parsed.path.lower()
        path_segments = [p for p in path.split("/") if p]

        # Parse Query Parameters
        query_params = parse_qs(parsed.query.lower())
        
        # Parse Fragment / Hash
        fragment = parsed.fragment.lower()

        # Token Extraction: Break down all segments by hyphens, underscores, dots, and slashes
        flagged_keywords: List[Dict[str, Any]] = []
        total_risk = 0
        reasons: List[str] = []

        def inspect_tokens_in_text(text: str, location: str):
            nonlocal total_risk
            # Tokenize by non-alphanumeric characters
            tokens = re.split(r"[-_./?=&%]+", text)
            for t in tokens:
                if not t or len(t) < 2:
                    continue
                for cat_key, cat_data in self.keyword_categories.items():
                    for target_token in cat_data["tokens"]:
                        # Exact token match or clear subtoken match
                        if t == target_token or target_token in t:
                            # Avoid duplicate logging of same keyword in same location
                            if not any(k["keyword"] == target_token and k["location"] == location for k in flagged_keywords):
                                flagged_keywords.append({
                                    "keyword": target_token,
                                    "detected_in": t,
                                    "category": cat_key,
                                    "category_label": cat_data["label"],
                                    "severity": cat_data["severity"],
                                    "weight": cat_data["base_weight"],
                                    "location": location
                                })
                                total_risk += cat_data["base_weight"]
                                reasons.append(f"[{location.upper()}] Detected {cat_data['label']} keyword: '{target_token}'")

        # 1. Scan Subdomains
        for sub in subdomains:
            inspect_tokens_in_text(sub, "subdomain")

        # 2. Scan Second-Level Domain
        inspect_tokens_in_text(domain, "domain")

        # 3. Scan Path Segments
        for seg in path_segments:
            inspect_tokens_in_text(seg, "path")

        # 4. Scan Query Parameters (both keys and values)
        for q_key, q_vals in query_params.items():
            inspect_tokens_in_text(q_key, f"query_param_key({q_key})")
            for qv in q_vals:
                inspect_tokens_in_text(qv, f"query_param_val({q_key})")

        # 5. Scan Fragment
        if fragment:
            inspect_tokens_in_text(fragment, "fragment")

        # 6. Structural & Protocol Anomaly Checks
        # A. Raw IP Address host
        is_ip = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host))
        if is_ip:
            total_risk += 45
            reasons.append("[HOST] Raw numeric IP host used instead of verified domain name")

        # B. HTTP Basic Auth deception (@ sign in netloc)
        if has_auth_abuse:
            total_risk += 60
            reasons.append(f"[DECEPTION] HTTP Basic Auth '@' hijack: pretends to be '{netloc.split('@')[0]}'")

        # C. Subdomain Brand Spoofing (e.g. paypal.com.attacker.xyz)
        subdomain_str = ".".join(subdomains)
        brand_spoofed = None
        for brand in self.monitored_brands:
            if brand in subdomain_str:
                brand_spoofed = brand
                total_risk += 65
                reasons.append(f"[SUBDOMAIN HIJACK] Embeds trusted brand '{brand.title()}' inside external domain ({host})")
                break

        # D. Domain Homoglyph / Leetspeak
        if not brand_spoofed:
            for brand, official in self.monitored_brands.items():
                if brand in domain and not (host == official or host.endswith("." + official)):
                    total_risk += 50
                    reasons.append(f"[DOMAIN SPOOF] Contains brand name '{brand.title()}' on unverified root domain")
                    break

        # D2. Typosquatting / Leetspeak Normalization (paypa1→paypal, g00gle→google etc.)
        _leet_map = str.maketrans("10305@$!", "loeoasil")
        _leet_domain = domain.translate(_leet_map)
        if not brand_spoofed and _leet_domain != domain:
            for brand, official in self.monitored_brands.items():
                if brand in _leet_domain and not (host == official or host.endswith("." + official)):
                    total_risk += 65
                    reasons.append(f"[TYPOSQUAT] Leetspeak/numeric substitution mimics '{brand.title()}' brand: '{domain}' -> '{_leet_domain}'")
                    brand_spoofed = brand
                    break

        # E. Subdomain Lure Stacking (e.g. win.prizepool.safari.money.com)
        lure_tokens_in_subdomains = [
            k for k in flagged_keywords if k["location"] == "subdomain"
        ]
        if len(lure_tokens_in_subdomains) >= 2:
            total_risk += 50
            reasons.append(f"[SUBDOMAIN LURE STACKING] Suspicious multi-lure subdomain chain: '{', '.join(k['keyword'] for k in lure_tokens_in_subdomains)}'")

        # F. Abusive TLD Check
        is_abusive_tld = tld in self.abusive_tlds
        if is_abusive_tld:
            total_risk += 35
            reasons.append(f"[TLD] High-risk abusive Top-Level Domain: .{tld}")

        # G. Dangerous Payload Extension in Path (.apk, .exe, etc.)
        detected_payload = None
        for ext in [".apk", ".exe", ".scr", ".bat", ".vbs", ".js", ".iso", ".zip"]:
            if path.endswith(ext):
                detected_payload = ext
                total_risk += 65
                reasons.append(f"[PAYLOAD] Direct downloadable application/script: '{ext}'")
                break

        # H. Excessive Subdomain Chaining (> 2 levels)
        if len(subdomains) > 2:
            total_risk += 25
            reasons.append(f"[OBFUSCATION] Deep subdomain chaining ({len(subdomains)} levels: {'.'.join(subdomains)})")

        # I. RANDOM / GIBBERISH DOMAIN DETECTION
        # I1. Gibberish Second-Level Domain (e.g. capapccfffs.com, xkqzpwrt.tk)
        if self._is_gibberish(domain):
            total_risk += 55
            ent = round(self._shannon_entropy(domain), 2)
            reasons.append(
                f"[GIBBERISH DOMAIN] SLD '{domain}' appears randomly generated "
                f"(entropy={ent}, no natural vowel/consonant pattern)"
            )

        # I2. High-Entropy Random Path Segments (e.g. /aBf93Qk7Px2/)
        for seg in path_segments:
            seg_entropy = self._shannon_entropy(seg)
            has_mixed_case_digits = bool(re.search(r'[A-Z]', seg)) and bool(re.search(r'\d', seg))
            if len(seg) >= 8 and seg_entropy >= 3.5 and has_mixed_case_digits:
                total_risk += 35
                reasons.append(
                    f"[RANDOM PATH TOKEN] Path segment '{seg[:20]}' looks like a "
                    f"machine-generated random token (entropy={round(seg_entropy,2)})"
                )
                break  # One detection is enough

        # I3. Gibberish Subdomain (e.g. xkqz.bank-update.com)
        for sub in subdomains:
            if self._is_gibberish(sub):
                ent = round(self._shannon_entropy(sub), 2)
                total_risk += 40
                reasons.append(
                    f"[GIBBERISH SUBDOMAIN] Subdomain '{sub}' appears randomly generated "
                    f"(entropy={ent}) — DGA/bot-generated domain pattern"
                )
                break

        # I4. Very long domain name (obfuscation via length)
        if len(domain) >= 20:
            total_risk += 20
            reasons.append(
                f"[LONG DOMAIN] Unusually long SLD ('{domain[:25]}...', len={len(domain)}) "
                f"— common in scam domains to bury legitimate-looking words"
            )

        # I5. Purely numeric or alphanumeric-only domain (no real word)
        if re.match(r'^[a-z0-9]{6,}$', domain) and not any(v in domain for v in 'aeiou'):
            total_risk += 30
            reasons.append(
                f"[NO-VOWEL DOMAIN] SLD '{domain}' contains no vowels "
                f"— hallmark of auto-generated scam/C2 domains"
            )

        # Normalization of overall score (0 to 100)
        overall_score = min(total_risk, 100)

        # Disposition & Safe Advice  (4-tier verdict)
        if overall_score >= 70:
            verdict = "CRITICAL_MALICIOUS"
            verdict_badge = "🚨 CRITICAL MALICIOUS PHISHING LINK"
        elif overall_score >= 50:
            verdict = "HIGH_RISK"
            verdict_badge = "🔴 HIGH-RISK SUSPICIOUS LINK"
        elif overall_score >= 25:
            verdict = "SUSPICIOUS"
            verdict_badge = "⚠️ SUSPICIOUS UNVERIFIED LINK"
        else:
            verdict = "SAFE"
            verdict_badge = "✅ BENIGN / SAFE LINK"

        # Construct Actionable Safe Advice
        if brand_spoofed:
            safe_advice = f"🚨 BRAND HIJACKING ALERT: This link uses '{brand_spoofed.title()}' inside its subdomain, but navigates to an unauthorized server ({host}). Visiting will harvest your credentials."
        elif detected_payload:
            safe_advice = f"🚨 DANGEROUS DOWNLOAD BLOCKED: Link directly delivers an executable payload ({detected_payload}). Do not install files from unverified external links."
        elif is_abusive_tld and len(flagged_keywords) > 0:
            top_kws = [k['keyword'] for k in flagged_keywords[:3]]
            safe_advice = f"🚨 PHISHING INDICATORS: Deceptive keywords ('{', '.join(top_kws)}') hosted on an abusive .{tld} domain. Do not proceed."
        elif len(flagged_keywords) > 0:
            top_kws = [k['keyword'] for k in flagged_keywords[:3]]
            safe_advice = f"⚠️ Exercise caution: URL contains high-risk intent tokens: {', '.join(top_kws)}."
        else:
            safe_advice = "No suspicious deception tokens or hostile domain signatures identified."

        return {
            "original_url": raw_url,
            "normalized_url": normalized,
            "anatomy": {
                "scheme": scheme,
                "host": host,
                "subdomains": subdomains,
                "domain": domain,
                "tld": tld,
                "port": port,
                "path": path,
                "path_segments": path_segments,
                "query_params": query_params,
                "fragment": fragment,
                "is_ip_host": is_ip,
                "is_abusive_tld": is_abusive_tld,
                "has_auth_abuse": has_auth_abuse,
                "payload_extension": detected_payload
            },
            "flagged_keywords": flagged_keywords,
            "total_keywords_detected": len(flagged_keywords),
            "threat_reasons": reasons,
            "composite_risk_score": overall_score,
            "risk_score": overall_score,          # alias for compatibility
            "verdict": verdict,
            "verdict_badge": verdict_badge,
            "safe_advice": safe_advice
        }

