from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class MessageCheckRequest(BaseModel):
    sender: str = Field(..., description="Phone number, email, or handle of the sender")
    sender_name: Optional[str] = Field(None, description="Display name claiming to be sender")
    content: str = Field(..., description="Message text content")
    channel: str = Field("SMS", description="Channel: SMS, WhatsApp, Telegram, Email, Social")

class LinkCheckRequest(BaseModel):
    url: str = Field(..., description="URL to be inspected before clicking")
    context: Optional[str] = Field(None, description="Surrounding message context if available")

class Contact(BaseModel):
    id: str
    name: str
    identifier: str  # Phone number or email
    relationship: str  # Family, Friend, Work, Verified Service
    trust_level: str = "TRUSTED"  # TRUSTED, VERIFIED, NEUTRAL
    added_at: str

class ContactCreate(BaseModel):
    name: str
    identifier: str
    relationship: str = "Friend"
    trust_level: str = "TRUSTED"

class ThreatIndicator(BaseModel):
    layer: str  # CONTACT_SENDER, NLP_CONTENT, LINK_PAYLOAD, APP_PAYLOAD
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    code: str
    description: str
    detail: Optional[str] = None

class ExtractedLinkResult(BaseModel):
    original_url: str
    normalized_url: str
    domain: str
    is_suspicious: bool
    risk_score: int
    threat_reasons: List[str] = []
    safe_destination_advice: Optional[str] = None

class ExtractedAppResult(BaseModel):
    filename: str
    extension: str
    is_executable: bool
    risk_score: int
    risk_type: str
    description: str

class SecurityAssessment(BaseModel):
    id: str
    timestamp: str
    sender: str
    sender_name: Optional[str] = None
    channel: str
    is_known_contact: bool
    overall_score: int  # 0 (Safe) to 100 (Critical Malicious)
    disposition: str  # SAFE, WARN, BLOCK
    action_banner: str
    summary: str
    recommendation: str
    indicators: List[ThreatIndicator] = []
    extracted_links: List[ExtractedLinkResult] = []
    extracted_apps: List[ExtractedAppResult] = []
    layer_scores: Dict[str, int] = {}

class TelemetryStats(BaseModel):
    total_inspected: int
    safe_count: int
    warn_count: int
    blocked_count: int
    malicious_links_caught: int
    dangerous_apps_stopped: int
    fake_offers_intercepted: int
    impersonations_detected: int

class Scenario(BaseModel):
    id: str
    title: str
    category: str  # Phishing, Lottery/Offer, Malicious App, CEO/Impersonation, Legitimate
    sender: str
    sender_name: str
    channel: str
    content: str
    description: str
    expected_disposition: str
