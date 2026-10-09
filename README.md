# SentinX — Smart Spam Detection & Security Layer
> **Protecting users from spam messages, links, and malicious applications before user interaction.**

---

## 🌟 Overview & Key Innovation

Traditional spam filters only **reactively block phone numbers or email addresses after the user has already been disturbed**. Spammers easily circumvent this by rotating numbers, spoofing caller IDs, and creating disposable accounts.

**SentinX introduces a proactive, pre-interaction defense architecture:**
1. **Pre-Interaction Interception (Slides 4 & 9)**: Evaluates incoming messages, URLs, and file attachments *before* the user opens, clicks, or interacts with them.
2. **Contact & Trust Graph (Slide 6)**: Distinguishes saved contacts in your address book from unknown sources. Trusted contacts are delivered without false friction, while unknown senders trigger **Deep Scrutiny Mode**.
3. **Pre-Click Link & App Guard (Slides 4 & 7)**: Inspects destination servers, domain typosquatting (`paypa1.click`), unmasks shorteners, and blocks direct malicious application downloads (`.apk`, `.exe`).
4. **Intent & Semantic NLP (Slides 2 & 5)**: Detects social engineering patterns—fake lottery wins, delivery fee scams, urgency coercion, and financial fraud—regardless of the sender's changing phone numbers.
5. **Safe User Suggestions & Warnings (Slide 7)**: Provides clear explanations and safe recommendations (e.g. pointing to authentic domains) to protect users.

---

## 🏗️ System Architecture

```
Incoming Message / Link / App
              │
              ▼
   ┌────────────────────────────────────────────────────────┐
   │ 1. Sender & Trust Graph Analyzer                      │
   │    • Address book verification                         │
   │    • Brand & display name impersonation detection      │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │ 2. Semantic NLP Intent Engine                          │
   │    • Fake offer / lottery reward cues                  │
   │    • Urgency / account suspension threats              │
   │    • Credential & OTP harvesting detection             │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │ 3. Pre-Click Link & Application Guard                  │
   │    • Typosquatting / homoglyph detection               │
   │    • High-risk TLDs (.xyz, .top, .click)               │
   │    • Raw numeric IP hosts & URL shortener unmasking    │
   │    • Malicious APK / executable download checks        │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │ 4. Composite Risk & Disposition Engine                 │
   │    • Score: 0 (Safe) to 100 (Critical Danger)          │
   │    • Action: SAFE / WARN / BLOCK                       │
   │    • Explainable indicators & Safe Recommendations     │
   └────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

- **Backend**: Python 3.9+, FastAPI, Pydantic v2, Uvicorn, Regex / NLP pattern engine
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons
- **Platform**: Multi-channel support (SMS, WhatsApp, Telegram, Email, Social DMs)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ installed
- Node.js v18+ and npm installed

### 2. Running with 1-Click (Windows)
Double-click `run_project.bat` in the project root. This starts both the FastAPI backend and React frontend automatically.

### 3. Running Manually

#### Backend:
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## 📱 Features & Demonstration Views

1. **📱 Device Shield Simulator (Mobile View)**:
   - Experience the pre-interaction layer popping up over a smartphone screen mockup.
   - Test 6 realistic 1-click attack and legitimate scenarios:
     - *Fake Offer & Lottery Scam ($1000 prize on .xyz domain)*
     - *Bank Fraud Alert Impersonation (Spoofing Chase with urgency)*
     - *Malicious APK Dropper (Unverified IP link to .apk trojan)*
     - *Fake USPS Delivery Redelivery Fee (Smishing on .top TLD)*
     - *Sister Message (Verified saved contact passing with 0 friction)*
     - *Colleague Work Document (Verified trusted link)*
   - Test clicking links inside the simulated phone to trigger the **Pre-Click Interception Modal**!

2. **🛡️ SOC Operations Center**:
   - Live telemetry counters: Total Interceptions, High Threats Blocked, Warnings Issued, Malicious Links Caught, Dangerous APKs Deflected, Impersonations Detected.
   - Comprehensive Threat Log table with clickable forensic details.

3. **🔗 Pre-Click Link Guard Tool**:
   - Paste any URL to evaluate destination risk, domain homoglyphs, and receive safe alternatives.

4. **👥 Contacts & Trust Graph Vault**:
   - Manage the address book to observe how saved contacts prevent false alarms while maintaining security.

---

## 📜 API Endpoints

- `POST /api/check-message`: Main pre-interaction security gateway (evaluates sender, content, links, and payloads).
- `POST /api/check-link`: Standalone pre-click link forensics endpoint.
- `GET /api/scenarios`: Returns pre-loaded realistic test attack scenarios.
- `GET /api/contacts`: Fetches contacts from the trust graph.
- `POST /api/contacts`: Adds a new contact.
- `DELETE /api/contacts/{id}`: Deletes a contact.
- `GET /api/telemetry`: Aggregated real-time metrics.
- `GET /api/threat-history`: Historical log of inspected messages.
- `POST /api/reset-telemetry`: Resets telemetry counters for live demos.
