import re
from typing import Dict, List, Tuple, Any

class ContentNLPEngine:
    """
    Enterprise-grade Semantic NLP & Threat Intelligence Lexicon Engine.
    Equipped with exhaustive pattern matching across modern scam vectors:
    - KYC & Banking Compliance Scams
    - Part-Time / Task / YouTube 'Like & Earn' Job Scams
    - Electricity & Utility Disconnection Threats
    - Instant Unverified Loan Approvals
    - Reward Points & Tax Refund / Cashback Scams
    - Telecom / SIM Card Deactivation
    - Crypto & Forex Doubling Schemes
    - Sextortion / Blackmail / Malware Intrusion
    - Law Enforcement / Digital Arrest Impersonation
    - Fake Offers, Lottery & Gift Cards
    - Urgency & Psychological Coercion
    - Credential & OTP / Seed-Phrase Harvesting
    """
    def __init__(self):
        self.categories = {
            "KYC_BANKING_COMPLIANCE": {
                "label": "KYC & Banking Compliance Fraud",
                "base_weight": 45,
                "description": "Deceptive requests to update KYC, PAN, or Aadhaar under threat of account freezing.",
                "keywords": [
                    "kyc", "pan card", "aadhaar", "re-kyc", "netbanking blocked", "debit card blocked",
                    "account suspended", "kyc expired", "update kyc", "link pan", "submit kyc"
                ],
                "patterns": [
                    r"\b(?:kyc|pan|pan\s*card|aadhaar)\b.*?\b(?:expired|mandatory|update|link|suspended|blocked|incomplete)\b",
                    r"\b(?:dear\s+customer)?\b.*?\b(?:bank|sbi|hdfc|icici|axis|pnb|paytm)\s+account\b.*?\b(?:blocked|freeze|suspended|disabled)\b",
                    r"\bto\s+(?:unblock|reactivate|verify)\s+(?:your)?\s*(?:netbanking|account|debit\s*card)\b",
                    r"\bcomplete\s+your\s+(?:e-kyc|re-kyc|kyc\s+verification)\b",
                    r"\bfailure\s+to\s+update\s+will\s+result\s+in\s+permanent\s+(?:closure|freeze)\b"
                ]
            },
            "JOB_TASK_SCAM": {
                "label": "Part-Time Task & Job Work Fraud",
                "base_weight": 40,
                "description": "Offers paying huge daily income for liking videos, rating products, or Telegram tasks.",
                "keywords": [
                    "part-time job", "work from home", "like youtube videos", "earn daily", "telegram task",
                    "daily payout", "rating products", "data entry", "hr manager", "guaranteed income"
                ],
                "patterns": [
                    r"\b(?:earn|make)\s+(?:\$|rs\.?|inr|usd)?\s*\d{3,5}\s*(?:-\s*\d{3,5})?\s*(?:daily|per\s+day|hourly)\b",
                    r"\b(?:part-time|work\s+from\s+home|freelance)\s+(?:job|opportunity|vacancy|position)\b",
                    r"\b(?:like|subscribe|rate)\s+(?:youtube|google|hotel|movie)\s+(?:videos|reviews|products)\b.*?\b(?:earn|get\s+paid)\b",
                    r"\bcontact\s+(?:our\s+)?(?:hr|manager|recruiter)\s+on\s+telegram\b",
                    r"\bno\s+(?:prior\s+)?experience\s+required\b.*?\b(?:daily\s+payment|instant\s+withdrawal)\b",
                    r"\btask\s+(?:completion|salary|commission)\s+(?:deposit|reward)\b"
                ]
            },
            "ELECTRICITY_UTILITY_SCAM": {
                "label": "Electricity / Utility Disconnection Threat",
                "base_weight": 50,
                "description": "False threats that electricity or gas will be disconnected due to unpaid bills.",
                "keywords": [
                    "electricity bill", "power disconnected", "light bill", "unpaid bill", "contact electricity officer",
                    "consumer number", "disconnection notice", "update bill", "pay bill immediately"
                ],
                "patterns": [
                    r"\belectricity\s+(?:power|connection|service)\s+will\s+be\s+(?:disconnected|cut\s*off|suspended)\b",
                    r"\b(?:tonight|today)\s+at\s+(?:\d{1,2}[:.]\d{2}\s*(?:pm|am)?|\d{1,2}\s*(?:pm|am))\b.*?\bbill\b",
                    r"\bprevious\s+month\s+bill\s+was\s+not\s+updated\b",
                    r"\bcontact\s+(?:our\s+)?electricity\s+(?:officer|helpline|support)\b",
                    r"\bcall\s+(?:our\s+)?power\s+department\b"
                ]
            },
            "LOAN_CREDIT_FRAUD": {
                "label": "Instant Unverified Loan / Credit Trap",
                "base_weight": 40,
                "description": "Pre-approved loans with no documentation or CIBIL checks designed to push predatory malware.",
                "keywords": [
                    "pre-approved loan", "instant loan", "0% interest", "no cibil required", "disbursement pending",
                    "personal loan approved", "download loan app", "instant cash"
                ],
                "patterns": [
                    r"\b(?:congratulations|approved)\b.*?\b(?:pre-approved|instant)\s+loan\s+of\s+(?:\$|rs\.?|inr|usd)?\s*\d+[\d,]*\b",
                    r"\bno\s+(?:cibil|credit\s+score|documents?|paperwork)\s+required\b",
                    r"\bloan\s+amount\s+ready\s+for\s+disbursal\b",
                    r"\binterest\s+rate\s+as\s+low\s+as\s+0(?:\.0)?%\b",
                    r"\bdownload\s+(?:our\s+)?(?:instant\s+)?loan\s+app\b"
                ]
            },
            "REWARD_POINTS_REFUND": {
                "label": "Reward Points & Tax Refund Expiry",
                "base_weight": 40,
                "description": "Scams claiming accumulated credit card points or tax refunds are expiring today.",
                "keywords": [
                    "reward points", "points expiring", "redeem points into cash", "tax refund", "cashback pending",
                    "credit card points", "claim refund", "unclaimed cashback"
                ],
                "patterns": [
                    r"\b(?:credit|debit)\s+card\s+reward\s+points?\s+(?:expiring|worth\s+(?:\$|rs\.?)\s*\d+)\b",
                    r"\bredeem\s+(?:your)?\s*points?\s+(?:into|as|for)\s+(?:cash|inr|usd|\$)\b",
                    r"\btax\s+refund\s+(?:of\s+(?:\$|rs\.?)\s*\d+[\d,]*\.?\d*)?\s+(?:pending|approved|ready)\b",
                    r"\bclaim\s+(?:your)?\s*(?:pending\s+)?cashback\s+(?:within\s+24\s*hours)?\b",
                    r"\bunclaimed\s+refund\s+will\s+expire\s+today\b"
                ]
            },
            "SIM_TELECOM_SCAM": {
                "label": "SIM Card / Telecom Deactivation Threat",
                "base_weight": 45,
                "description": "Threats that phone service or SIM card will be deactivated within hours.",
                "keywords": [
                    "sim card blocked", "esim upgrade", "sim verification", "telecom department", "trai notice",
                    "5g upgrade", "sim deactivation", "kyc for sim"
                ],
                "patterns": [
                    r"\b(?:sim\s+card|mobile\s+number)\s+will\s+be\s+(?:blocked|deactivated|disconnected|terminated)\b",
                    r"\b(?:trai|dot|telecom)\s+(?:department|notice|advisory)\b",
                    r"\b(?:esim|5g)\s+(?:upgrade|activation|request)\s+(?:pending|initiated)\b",
                    r"\bto\s+keep\s+your\s+(?:outgoing|services?)\s+active\b"
                ]
            },
            "CRYPTO_FOREX_PONZI": {
                "label": "High-Yield Crypto / Forex Ponzi Scheme",
                "base_weight": 45,
                "description": "Promises of unrealistic guaranteed returns or crypto wallet doubling.",
                "keywords": [
                    "guaranteed returns", "crypto trading bot", "double your investment", "forex signals",
                    "vip trading group", "mining pool profits", "binance airdrop", "seed phrase"
                ],
                "patterns": [
                    r"\bguaranteed\s+(?:\d{2,3}%|\d+x)\s+(?:profit|returns?|roi)\b",
                    r"\bdouble\s+your\s+(?:money|bitcoin|crypto|investment)\s+in\s+\d+\s*(?:hours|days)\b",
                    r"\bjoin\s+(?:our\s+)?(?:vip|exclusive)\s+(?:crypto|trading|forex)\s+(?:group|channel|signals)\b",
                    r"\bautomated\s+(?:ai\s+)?trading\s+bot\s+with\s+100%\s+win\s+rate\b",
                    r"\benter\s+(?:your)?\s*12[- ](?:word|secret)\s+(?:recovery|seed)\s+phrase\b"
                ]
            },
            "SEXTORTION_BLACKMAIL": {
                "label": "Sextortion & Malware Blackmail Threat",
                "base_weight": 55,
                "description": "False claims that the user's webcam was recorded or Pegasus spyware was installed.",
                "keywords": [
                    "recorded your webcam", "pegasus spyware", "private video", "send bitcoin", "leaking your video",
                    "hacked your device", "blackmail", "ransom payment"
                ],
                "patterns": [
                    r"\b(?:recorded|captured)\s+(?:a\s+)?(?:video|footage)\s+of\s+you\b",
                    r"\b(?:pegasus|trojan|malware|spyware)\s+(?:installed|infected)\s+(?:on\s+your\s+device)?\b",
                    r"\bsend\s+(?:\$?\d+[\d,]*\s*(?:in|worth\s+of)?\s*)?(?:btc|bitcoin|crypto)\s+to\s+(?:my)?\s*(?:wallet|address)\b",
                    r"\bi\s+will\s+send\s+(?:this|your)\s+(?:video|recording)\s+to\s+all\s+your\s+contacts\b"
                ]
            },
            "LAW_ENFORCEMENT_IMPERSONATION": {
                "label": "Law Enforcement & Digital Arrest Impersonation",
                "base_weight": 55,
                "description": "Scammers posing as police, CBI, or cyber crime officers threatening imminent arrest.",
                "keywords": [
                    "digital arrest", "cyber crime department", "cbi officer", "arrest warrant", "police summons",
                    "narcotics package seized", "court notice", "customs detention"
                ],
                "patterns": [
                    r"\b(?:digital\s+arrest|arrest\s+warrant|police\s+summon|court\s+notice)\b",
                    r"\b(?:cyber\s+crime|cbi|fbi|interpol|police)\s+(?:department|headquarters|officer)\b",
                    r"\bparcel\s+(?:containing|with)\s+(?:drugs|narcotics|passports|fake\s+ids)\s+seized\b",
                    r"\bcontact\s+immediately\s+to\s+avoid\s+(?:arrest|criminal\s+charges)\b"
                ]
            },
            "FAKE_OFFER_LOTTERY": {
                "label": "Lottery, Prize & Free Gift Fraud",
                "base_weight": 40,
                "description": "Bogus claims of winning lotteries, shopping vouchers, or iPhones.",
                "keywords": [
                    "congratulations won", "winner selected", "claim gift card", "spin the wheel", "jackpot payout",
                    "exclusive prize", "free iphone", "walmart winner", "amazon voucher"
                ],
                "patterns": [
                    r"\b(?:congratulations|congrats)\b",
                    r"\b(?:you(?:'ve|\s+have)?\s+won|you\s+are\s+a\s+winner|selected\s+as\s+a?\s*winner)\b",
                    r"\b(?:claim|redeem)\s+(?:your)?\s*(?:\$?\d+[\d,]*\s*(?:cash|gift card|voucher|reward|bonus|prize)?)\b",
                    r"\bexclusive\s+(?:deal|offer|prize|free gift)\b",
                    r"\byou(?:'ve|\s+have)\s+been\s+(?:chosen|selected)\b",
                    r"\bspin\s+(?:the\s+wheel|to\s+win)\b",
                    r"\b(?:guaranteed|instant)\s+(?:payout|reward|jackpot)\b",
                    r"\b(?:free|gift)\s+(?:card|iphone|cash|voucher|reward)\b",
                    r"\b(?:\$\d+[\d,]*|\d+\s*(?:dollars|usd))\s+(?:gift\s+card|prize|cash|reward|winner)\b"
                ]
            },
            "URGENCY_COERCION": {
                "label": "Urgency, Fear & Coercion Tactics",
                "base_weight": 40,
                "description": "High-pressure deadlines designed to bypass rational thinking.",
                "keywords": [
                    "account suspended", "immediate action required", "final warning", "within 24 hours",
                    "unauthorized access", "action required", "urgent notice", "service termination"
                ],
                "patterns": [
                    r"\b(?:account|access|service)\s+(?:suspended|locked|blocked|terminated|cancelled)\b",
                    r"\bwithin\s+(?:24|12|48|2|1)\s*(?:hours|hrs|minutes|mins)\b",
                    r"\bimmediate(?:ly)?\s+(?:action|verification|attention|response)\s+required\b",
                    r"\bfinal\s+(?:notice|warning|reminder)\b",
                    r"\bto\s+avoid\s+(?:suspension|termination|permanent\s+closure|legal\s+action)\b",
                    r"\bunauthorized\s+(?:sign-in|activity|transaction|access)\s+detected\b",
                    r"\baction\s+required\b",
                    r"\burgent\b"
                ]
            },
            "CREDENTIAL_OTP_HARVEST": {
                "label": "Credential & OTP Harvesting Pattern",
                "base_weight": 50,
                "description": "Direct attempts to steal login credentials, one-time passwords, or PINs.",
                "keywords": [
                    "share otp", "send verification code", "verify identity", "password reset", "banking login",
                    "pin code", "do not share this code", "confirm credentials"
                ],
                "patterns": [
                    r"\b(?:send|reply\s+with|share)\s+(?:your)?\s*(?:otp|code|pin|password|passcode)\b",
                    r"\bverify\s+your\s+(?:identity|account|credentials|ssn|social\s+security)\b",
                    r"\bupdate\s+your\s+(?:security\s+details|billing\s+information)\b",
                    r"\bdo\s+not\s+share\s+this\s+code\b.*?\b(?:send\s+to|reply)\b"
                ]
            }
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes message text against the expanded threat categories.
        """
        if not text:
            return {
                "nlp_score": 0,
                "matched_categories": [],
                "highlights": [],
                "summary": "Clean message content."
            }

        total_score = 0
        matched_categories = []
        highlights = []
        text_lower = text.lower()

        for cat_name, data in self.categories.items():
            cat_matched = False
            matched_snippets = []

            # 1. Regex Pattern check
            for pattern in data["patterns"]:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for m in matches:
                    matched_text = m.group(0)
                    if matched_text not in highlights:
                        highlights.append(matched_text)
                    if matched_text not in matched_snippets:
                        matched_snippets.append(matched_text)
                    cat_matched = True

            # 2. Keyword exact match check
            for kw in data.get("keywords", []):
                if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                    if kw not in highlights:
                        highlights.append(kw)
                    if kw not in matched_snippets:
                        matched_snippets.append(kw)
                    cat_matched = True

            if cat_matched:
                total_score += data["base_weight"]
                matched_categories.append({
                    "category": cat_name,
                    "label": data["label"],
                    "weight": data["base_weight"],
                    "description": data["description"],
                    "matched_terms": matched_snippets[:4]
                })

        # Heuristic modifiers: Excessive capitalization, exclamation marks
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.4 and len(text) > 30:
            total_score += 15
            highlights.append("EXCESSIVE_CAPITALIZATION")

        exclamation_count = text.count("!")
        if exclamation_count >= 3:
            total_score += 10
            highlights.append("EXCESSIVE_EXCLAMATIONS")

        # Bound score between 0 and 100
        normalized_score = min(total_score, 100)

        # Build human-readable summary
        if normalized_score == 0:
            summary = "No suspicious social engineering, fraud keywords, or scam patterns detected in message body."
        elif normalized_score < 40:
            summary = f"Low-level promotional cues identified ({len(matched_categories)} pattern category)."
        elif normalized_score < 75:
            summary = f"Suspicious cues detected: {', '.join(c['label'] for c in matched_categories[:2])}."
        else:
            summary = f"High-risk scam intent detected: {', '.join(c['label'] for c in matched_categories[:3])}."

        return {
            "nlp_score": normalized_score,
            "matched_categories": matched_categories,
            "highlights": highlights,
            "summary": summary
        }

    def get_lexicon_catalog(self) -> List[Dict[str, Any]]:
        """Returns the full catalog of threat categories, keywords, and descriptions for UI display."""
        catalog = []
        for cat_key, data in self.categories.items():
            catalog.append({
                "id": cat_key,
                "label": data["label"],
                "base_weight": data["base_weight"],
                "description": data["description"],
                "keywords": data.get("keywords", [])
            })
        return catalog
