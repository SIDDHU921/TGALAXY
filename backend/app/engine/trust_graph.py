import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from app.models.schemas import Contact, ContactCreate

class TrustGraphEngine:
    """
    Evaluates sender identity against the user's address book / contact graph.
    Distinguishes known trusted contacts from unknown/suspicious numbers or spoofed identities.
    """
    def __init__(self):
        # In-memory contacts repository initialized with realistic default contacts
        self.contacts: Dict[str, Contact] = {}
        self._seed_default_contacts()
        
        # High-profile brand entities frequently impersonated by scammers
        self.monitored_brands = [
            "amazon", "paypal", "apple", "microsoft", "google", "netflix",
            "chase", "bank of america", "wells fargo", "citi", "capital one",
            "usps", "fedex", "dhl", "ups", "irs", "internal revenue",
            "whatsapp", "telegram", "facebook", "instagram", "geek squad"
        ]

    def _seed_default_contacts(self):
        default_list = [
            Contact(
                id="cnt-1",
                name="Sarah Jenkins",
                identifier="+1 (555) 234-5678",
                relationship="Family / Sister",
                trust_level="TRUSTED",
                added_at="2025-01-15 09:30"
            ),
            Contact(
                id="cnt-2",
                name="Alex Rivera",
                identifier="+1 (555) 876-5432",
                relationship="Colleague / Tech Lead",
                trust_level="TRUSTED",
                added_at="2025-02-10 14:15"
            ),
            Contact(
                id="cnt-3",
                name="Dr. Lisa Bennett",
                identifier="+1 (555) 345-6789",
                relationship="Healthcare Provider",
                trust_level="VERIFIED",
                added_at="2025-03-01 11:00"
            ),
            Contact(
                id="cnt-4",
                name="Official Bank Fraud Alerts",
                identifier="888222",
                relationship="Verified Shortcode",
                trust_level="VERIFIED",
                added_at="2025-01-01 08:00"
            )
        ]
        for c in default_list:
            norm = self._normalize_identifier(c.identifier)
            self.contacts[norm] = c

    def _normalize_identifier(self, identifier: str) -> str:
        """Strip non-alphanumeric characters for phones, lowercase for emails."""
        if not identifier:
            return ""
        ident = identifier.strip().lower()
        if "@" in ident:
            return ident
        # Strip phone formatting: +1 (555) 234-5678 -> 15552345678
        digits = re.sub(r"[^\d]", "", ident)
        # Remove leading '1' for US numbers if 11 digits to match 10-digit format
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
        return digits if digits else ident

    def is_known_contact(self, identifier: str) -> Tuple[bool, Optional[Contact]]:
        norm = self._normalize_identifier(identifier)
        if norm in self.contacts:
            return True, self.contacts[norm]
        
        # Check partial match on raw identifier
        for key, contact in self.contacts.items():
            if norm and norm in key:
                return True, contact
        return False, None

    def detect_impersonation(self, sender: str, sender_name: Optional[str], content: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detects if an unknown sender is impersonating a well-known service, brand, or financial institution.
        """
        is_known, _ = self.is_known_contact(sender)
        if is_known:
            return False, None, None

        text_to_check = f"{sender_name or ''} {content}".lower()
        
        for brand in self.monitored_brands:
            # Check if brand appears in sender display name or strong greeting/claim
            if sender_name and brand in sender_name.lower():
                return True, brand.title(), f"Sender name claims to be '{sender_name}' but originates from an unverified number ({sender})"
            
            # Check if text claims to be official notice from brand
            patterns = [
                rf"\b(from|official|security team|support|alert from|notice from)\s+{brand}\b",
                rf"\b{brand}\s+(security|alert|fraud department|customer service|suspended)\b"
            ]
            for pattern in patterns:
                if re.search(pattern, text_to_check):
                    return True, brand.title(), f"Message claims to be from {brand.title()} but originates from unverified external sender ({sender})"

        return False, None, None

    def get_all_contacts(self) -> List[Contact]:
        return list(self.contacts.values())

    def add_contact(self, new_c: ContactCreate) -> Contact:
        import uuid
        norm = self._normalize_identifier(new_c.identifier)
        contact = Contact(
            id=f"cnt-{uuid.uuid4().hex[:6]}",
            name=new_c.name,
            identifier=new_c.identifier,
            relationship=new_c.relationship,
            trust_level=new_c.trust_level,
            added_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.contacts[norm] = contact
        return contact

    def delete_contact(self, contact_id: str) -> bool:
        for key, c in list(self.contacts.items()):
            if c.id == contact_id:
                del self.contacts[key]
                return True
        return False
