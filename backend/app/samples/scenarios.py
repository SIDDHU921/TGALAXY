from typing import List
from app.models.schemas import Scenario

SCENARIOS: List[Scenario] = [
    Scenario(
        id="scen-1",
        title="Fake Offer & Lottery Scam (SMS)",
        category="Lottery / Fake Offer",
        sender="+1 (917) 555-0199",
        sender_name="Walmart Rewards",
        channel="SMS",
        content="CONGRATULATIONS! You have been selected as our Walmart $1,000 gift card winner. Claim your prize now at http://walmart-winner-card.xyz before it expires in 12 hours!",
        description="Classic lottery/prize lure with high-pressure deadline and suspicious .xyz domain.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-2",
        title="Bank Fraud Alert Impersonation (SMS)",
        category="Brand Impersonation / Phishing",
        sender="+1 (415) 555-7823",
        sender_name="Chase Fraud Alert",
        channel="SMS",
        content="Chase Fraud Alert: An unauthorized transaction of $982.50 was debited. If you did not authorize this, verify your identity immediately at https://chase-security-update.click/verify-login to avoid permanent account suspension.",
        description="Intimidation and fear tactic spoofing Chase Bank, driving victim to a credential harvesting lookalike link.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-3",
        title="KYC & PAN Card Expiry Banking Fraud (SMS)",
        category="KYC & Banking Compliance",
        sender="+1 (408) 555-8821",
        sender_name="Bank Alert Desk",
        channel="SMS",
        content="Dear Customer, your Bank NetBanking account will be blocked today because your KYC has expired. Complete your re-KYC and update PAN immediately at https://secure-banking-kyc-update.site/login to avoid service freeze.",
        description="High-frequency banking fraud leveraging KYC expiry and pan card linking threats to steal netbanking logins.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-4",
        title="Electricity Power Disconnection Threat (SMS)",
        category="Utility / Electricity Threat",
        sender="+1 (212) 555-6677",
        sender_name="Power Supply Office",
        channel="SMS",
        content="URGENT: Your electricity power connection will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Contact power officer immediately or pay bill at http://power-bill-update.online/pay-bill.",
        description="High-stress utility scam claiming immediate power cut-off unless fake bill payment is submitted.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-5",
        title="YouTube 'Like & Earn' Part-Time Job Scam (WhatsApp)",
        category="Part-Time Job / Task Fraud",
        sender="+44 7911 123456",
        sender_name="HR Manager Lisa",
        channel="WhatsApp",
        content="Hello! We have a simple work from home opportunity. Like YouTube videos and earn $200 - $500 daily with instant withdrawal. No experience required. Join our Telegram task group at https://telegram-job-reward.click/task-portal to claim your bonus.",
        description="Prevalent task scam offering daily payouts for liking videos, luring victims into Telegram investment traps.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-6",
        title="Credit Card Reward Points Expiry Scam (SMS)",
        category="Reward Points / Cashback",
        sender="+1 (617) 555-3344",
        sender_name="Card Reward Desk",
        channel="SMS",
        content="Dear Customer, your Credit Card reward points worth $450 are expiring today. Redeem your points into cash before midnight at https://card-rewards-redeem-cash.top/redeem-points.",
        description="Exploits fear of missing out on accumulated rewards to phish credit card details.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-7",
        title="Malicious Application (.APK) Dropper (WhatsApp)",
        category="Malicious App / APK Payload",
        sender="+44 7700 900123",
        sender_name="Security Team",
        channel="WhatsApp",
        content="URGENT: Install our mandatory security patch BankSecure_Update.apk from http://45.134.22.10/BankSecure_Update.apk to keep your account active and avoid service cancellation.",
        description="Sideloading attack attempting to trick user into installing a malicious Android APK directly from a raw numeric IP address.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-8",
        title="Fake USPS Delivery Redelivery Fee (SMS)",
        category="Fake Delivery / Smishing",
        sender="+1 (312) 555-4411",
        sender_name="USPS Tracking",
        channel="SMS",
        content="USPS: Your package cannot be delivered due to incomplete street address information. Pay a $2.95 redelivery fee at https://usps-tracking-redeliver.top to release your parcel.",
        description="Mass delivery smishing campaign harvesting credit card details via a low-cost fraudulent TLD.",
        expected_disposition="BLOCK"
    ),
    Scenario(
        id="scen-9",
        title="Trusted Contact: Family Message (WhatsApp)",
        category="Legitimate / Saved Contact",
        sender="+1 (555) 234-5678",
        sender_name="Sarah Jenkins",
        channel="WhatsApp",
        content="Hey! Are we still meeting for lunch tomorrow around 1:00 PM? Mom asked if you can bring the dessert on your way over.",
        description="Message from a verified saved contact. The system suppresses false alarms and allows normal friction-free delivery.",
        expected_disposition="SAFE"
    ),
    Scenario(
        id="scen-10",
        title="Trusted Colleague with Official Link (Telegram)",
        category="Legitimate / Verified Link",
        sender="+1 (555) 876-5432",
        sender_name="Alex Rivera",
        channel="Telegram",
        content="Here is the revised quarterly roadmap document for our client presentation: https://google.com/docs. Let me know your thoughts on slide 4.",
        description="Trusted colleague sharing an authentic official link. Evaluated and confirmed safe.",
        expected_disposition="SAFE"
    )
]

def get_all_scenarios() -> List[Scenario]:
    return SCENARIOS
