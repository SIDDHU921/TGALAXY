import os
import sys
import json
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Add backend directory to sys.path so we can import the core engine directly or call API
BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.engine.trust_graph import TrustGraphEngine
from app.engine.content_nlp import ContentNLPEngine
from app.engine.link_guard import LinkGuardEngine
from app.engine.decision_engine import SecurityDecisionEngine
from app.engine.url_keyword_deep_analyzer import DeepLinkKeywordAnalyzer
from app.models.schemas import MessageCheckRequest
from app.samples.scenarios import get_all_scenarios

class SentinXDesktopTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SentinX Shield — Desktop Security Layer Test App")
        self.root.geometry("980x740")
        self.root.minsize(860, 640)
        self.root.configure(bg="#0b1120")

        # Initialize core security engines directly
        self.trust_graph = TrustGraphEngine()
        self.nlp_engine = ContentNLPEngine()
        self.link_guard = LinkGuardEngine()
        self.decision_engine = SecurityDecisionEngine(self.trust_graph, self.nlp_engine, self.link_guard)
        self.deep_analyzer = DeepLinkKeywordAnalyzer()
        self.scenarios = get_all_scenarios()

        self._setup_styles()
        self._build_header()
        self._build_notebook()
        self._build_footer()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure dark colors
        self.style.configure(".", background="#0b1120", foreground="#f8fafc", font=("Segoe UI", 10))
        self.style.configure("TNotebook", background="#0b1120", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1e293b", foreground="#94a3b8", padding=[16, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#0284c7")], foreground=[("selected", "#ffffff")])

        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("Card.TFrame", background="#1e293b", relief="flat")
        self.style.configure("TLabelframe", background="#0f172a", foreground="#38bdf8", font=("Segoe UI", 10, "bold"), borderwidth=1)
        self.style.configure("TLabelframe.Label", background="#0f172a", foreground="#38bdf8", font=("Segoe UI", 10, "bold"))
        
        self.style.configure("Primary.TButton", background="#0284c7", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        self.style.map("Primary.TButton", background=[("active", "#0369a1")])
        
        self.style.configure("Danger.TButton", background="#be123c", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        self.style.map("Danger.TButton", background=[("active", "#9f1239")])

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#0f172a", height=70, padx=20, pady=10)
        header_frame.pack(fill="x", side="top")

        title_label = tk.Label(
            header_frame,
            text="🛡️ SentinX Shield — Security Layer Test Client",
            font=("Segoe UI", 15, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        )
        title_label.pack(side="left")

        badge = tk.Label(
            header_frame,
            text="PRE-INTERACTION ACTIVE",
            font=("Segoe UI", 9, "bold"),
            bg="#064e3b",
            fg="#34d399",
            padx=10,
            pady=3
        )
        badge.pack(side="right")

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=10)

        # Tab 1: Message Interceptor
        self.tab_msg = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_msg, text="📱 Message Interceptor")
        self._build_message_tab()

        # Tab 2: Deep Link Keyword Dissector
        self.tab_link = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_link, text="🔗 Deep URL Forensics")
        self._build_link_tab()

        # Tab 3: Dangerous Payload / File Scanner
        self.tab_payload = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_payload, text="📁 Payload & APK Scanner")
        self._build_payload_tab()

    def _build_message_tab(self):
        paned = tk.PanedWindow(self.tab_msg, orient="horizontal", bg="#0b1120", bd=0, sashwidth=6)
        paned.pack(fill="both", expand=True, padx=6, pady=6)

        # Left Column: Inputs & Scenarios
        left_frame = tk.Frame(paned, bg="#0f172a", padx=12, pady=12)
        paned.add(left_frame, minsize=400)

        # Scenario Picker
        tk.Label(left_frame, text="Select Preset Threat Scenario:", font=("Segoe UI", 10, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.scen_var = tk.StringVar()
        scen_titles = [s.title for s in self.scenarios]
        self.scen_combo = ttk.Combobox(left_frame, textvariable=self.scen_var, values=scen_titles, state="readonly")
        self.scen_combo.pack(fill="x", pady=(4, 12))
        self.scen_combo.bind("<<ComboboxSelected>>", self._on_scenario_selected)

        # Sender Identifier
        tk.Label(left_frame, text="Sender Phone / Email:", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.sender_entry = tk.Entry(left_frame, bg="#1e293b", fg="#f8fafc", insertbackground="#38bdf8", font=("Consolas", 10), bd=1, relief="solid")
        self.sender_entry.pack(fill="x", pady=(2, 8))

        # Claimed Name
        tk.Label(left_frame, text="Claimed Display Name:", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.name_entry = tk.Entry(left_frame, bg="#1e293b", fg="#f8fafc", insertbackground="#38bdf8", font=("Segoe UI", 10), bd=1, relief="solid")
        self.name_entry.pack(fill="x", pady=(2, 8))

        # Channel
        tk.Label(left_frame, text="Channel / App:", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.chan_var = tk.StringVar(value="SMS")
        chan_combo = ttk.Combobox(left_frame, textvariable=self.chan_var, values=["SMS", "WhatsApp", "Telegram", "Email", "Social DM"], state="readonly")
        chan_combo.pack(fill="x", pady=(2, 8))

        # Content
        tk.Label(left_frame, text="Message Body (text + links + .apk):", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.content_text = tk.Text(left_frame, height=7, bg="#1e293b", fg="#f8fafc", insertbackground="#38bdf8", font=("Consolas", 9), bd=1, relief="solid")
        self.content_text.pack(fill="both", expand=True, pady=(2, 10))

        # Inspect Button
        btn_scan = tk.Button(
            left_frame,
            text="⚡ Run Pre-Interaction Interception",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._run_message_scan
        )
        btn_scan.pack(fill="x")

        # Right Column: Live Interception Output & IOCs
        right_frame = tk.Frame(paned, bg="#0f172a", padx=12, pady=12)
        paned.add(right_frame, minsize=440)

        # Disposition Banner
        self.dispo_banner = tk.Label(
            right_frame,
            text="STATUS: READY FOR SCAN",
            font=("Segoe UI", 12, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
            padx=12,
            pady=10,
            relief="groove"
        )
        self.dispo_banner.pack(fill="x", pady=(0, 10))

        # Score & Contact Label
        self.meta_label = tk.Label(
            right_frame,
            text="Threat Score: 0/100 | Contact: Unknown",
            font=("Consolas", 10),
            bg="#0f172a",
            fg="#cbd5e1"
        )
        self.meta_label.pack(anchor="w", pady=(0, 6))

        # Recommendation Box
        tk.Label(right_frame, text="Safe User Recommendation:", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#38bdf8").pack(anchor="w")
        self.recom_box = tk.Label(
            right_frame,
            text="Select or enter a message to review real-time security actions.",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#f1f5f9",
            wraplength=420,
            justify="left",
            padx=8,
            pady=8,
            relief="solid",
            bd=1
        )
        self.recom_box.pack(fill="x", pady=(2, 10))

        # Indicators List
        tk.Label(right_frame, text="Flagged Indicators of Compromise (IOCs):", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        self.ioc_listbox = tk.Listbox(right_frame, bg="#1e293b", fg="#f8fafc", selectbackground="#0284c7", font=("Consolas", 9), bd=1, relief="solid")
        self.ioc_listbox.pack(fill="both", expand=True, pady=(2, 10))

        # Initialize with first scenario
        if self.scenarios:
            self.scen_combo.current(0)
            self._on_scenario_selected(None)

    def _on_scenario_selected(self, event):
        idx = self.scen_combo.current()
        if 0 <= idx < len(self.scenarios):
            s = self.scenarios[idx]
            self.sender_entry.delete(0, tk.END)
            self.sender_entry.insert(0, s.sender)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, s.sender_name)
            self.chan_var.set(s.channel)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", s.content)
            self._run_message_scan()

    def _run_message_scan(self):
        req = MessageCheckRequest(
            sender=self.sender_entry.get().strip() or "+15550000000",
            sender_name=self.name_entry.get().strip() or None,
            channel=self.chan_var.get(),
            content=self.content_text.get("1.0", tk.END).strip()
        )
        res = self.decision_engine.assess_message(req)

        # Update banner
        if res.disposition == "BLOCK":
            self.dispo_banner.config(text="🛡️ PRE-INTERACTION INTERCEPT: HIGH THREAT BLOCKED", bg="#881337", fg="#fecdd3")
        elif res.disposition == "WARN":
            self.dispo_banner.config(text="⚠️ ADVISORY WARNING: SUSPICIOUS ACTIVITY DETECTED", bg="#78350f", fg="#fde68a")
        else:
            self.dispo_banner.config(text="✅ VERIFIED SAFE: DELIVERED NORMALLY", bg="#064e3b", fg="#6ee7b7")

        contact_status = "Saved Contact (Trusted)" if res.is_known_contact else "Unknown Sender (Deep Scrutiny)"
        self.meta_label.config(text=f"Threat Score: {res.overall_score}/100 | Contact: {contact_status}")
        self.recom_box.config(text=res.recommendation)

        # Update IOCs
        self.ioc_listbox.delete(0, tk.END)
        for ind in res.indicators:
            self.ioc_listbox.insert(tk.END, f"[{ind.severity}] {ind.description}")
            if ind.detail:
                self.ioc_listbox.insert(tk.END, f"   -> {ind.detail}")

    def _build_link_tab(self):
        frame = tk.Frame(self.tab_link, bg="#0f172a", padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="URL to Analyze (Any Deceptive or Phishing Link):", font=("Segoe UI", 10, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")
        
        input_row = tk.Frame(frame, bg="#0f172a")
        input_row.pack(fill="x", pady=(4, 10))

        self.link_entry = tk.Entry(input_row, bg="#1e293b", fg="#f8fafc", insertbackground="#38bdf8", font=("Consolas", 10), bd=1, relief="solid")
        self.link_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.link_entry.insert(0, "https://paypal.com.account-update.xyz/login/verify-kyc?ref=telegram")

        btn_dissect = tk.Button(
            input_row,
            text="Dissect Link Keywords",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._run_link_dissection
        )
        btn_dissect.pack(side="right")

        # Quick preset buttons
        preset_frame = tk.Frame(frame, bg="#0f172a")
        preset_frame.pack(fill="x", pady=(0, 12))
        tk.Label(preset_frame, text="Quick Presets:", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b").pack(side="left", padx=(0, 6))

        presets = [
            ("Safari PrizePool Scam", "https://win.prizepool.safari.money.com/"),
            ("PayPal Subdomain Phish", "https://paypal.com.account-update.xyz/login/verify-kyc?ref=telegram"),
            ("APK Dropper", "http://192.168.1.10/BankSecure_Update.apk?download=instant"),
            ("Electricity Scam", "https://power-bill-payment.online/electricity/pay-bill?consumer=99281"),
            ("Safe Google Docs", "https://google.com/docs/presentation")
        ]
        for name, p_url in presets:
            b = tk.Button(
                preset_frame,
                text=name,
                font=("Segoe UI", 8),
                bg="#1e293b",
                fg="#38bdf8",
                bd=1,
                relief="solid",
                cursor="hand2",
                command=lambda u=p_url: self._load_and_scan_link(u)
            )
            b.pack(side="left", padx=3)

        # Output Text Box for Deep Anatomy
        self.link_output = tk.Text(frame, bg="#1e293b", fg="#f8fafc", font=("Consolas", 10), padx=10, pady=10, bd=1, relief="solid")
        self.link_output.pack(fill="both", expand=True)

        self._run_link_dissection()

    def _load_and_scan_link(self, target_url):
        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, target_url)
        self._run_link_dissection()

    def _run_link_dissection(self):
        url = self.link_entry.get().strip()
        if not url:
            return
        report = self.deep_analyzer.dissect_url(url)
        
        self.link_output.delete("1.0", tk.END)
        self.link_output.insert(tk.END, f"=========================================================================\n")
        self.link_output.insert(tk.END, f"  FORENSIC URL ANATOMY & KEYWORD DISSECTION REPORT\n")
        self.link_output.insert(tk.END, f"=========================================================================\n\n")
        self.link_output.insert(tk.END, f"TARGET URL: {report['normalized_url']}\n")
        self.link_output.insert(tk.END, f"VERDICT:    {report['verdict_badge']}\n")
        self.link_output.insert(tk.END, f"RISK SCORE: {report['composite_risk_score']} / 100\n\n")

        self.link_output.insert(tk.END, f"[1] STRUCTURAL ANATOMY BREAKDOWN:\n")
        anatomy = report["anatomy"]
        self.link_output.insert(tk.END, f"  - Protocol:         {anatomy['scheme']}://\n")
        self.link_output.insert(tk.END, f"  - Subdomain(s):     {'.'.join(anatomy['subdomains']) if anatomy['subdomains'] else '(None)'}\n")
        self.link_output.insert(tk.END, f"  - Root Domain:      {anatomy['domain']}\n")
        self.link_output.insert(tk.END, f"  - Top-Level Domain: .{anatomy['tld']} (Abusive TLD: {anatomy['is_abusive_tld']})\n")
        self.link_output.insert(tk.END, f"  - Path:             {anatomy['path']}\n")
        self.link_output.insert(tk.END, f"  - Query Parameters: {json.dumps(anatomy['query_params'])}\n")
        self.link_output.insert(tk.END, f"  - Payload Detected: {anatomy['payload_extension'] or '(None)'}\n\n")

        self.link_output.insert(tk.END, f"[2] DETECTED FRAUD & PHISHING KEYWORDS ({report['total_keywords_detected']}):\n")
        if report["flagged_keywords"]:
            for kw in report["flagged_keywords"]:
                self.link_output.insert(tk.END, f"  • KEYWORD: '{kw['keyword']}' (Location: {kw['location']}) | Weight: +{kw['weight']}\n")
                self.link_output.insert(tk.END, f"    Class:   {kw['category_label']} [{kw['severity']}]\n")
        else:
            self.link_output.insert(tk.END, f"  • (No deceptive keywords matched)\n")

        self.link_output.insert(tk.END, f"\n[3] STRUCTURAL VIOLATIONS / IOCs ({len(report['threat_reasons'])}):\n")
        for r in report["threat_reasons"]:
            self.link_output.insert(tk.END, f"  ⚠ {r}\n")

        self.link_output.insert(tk.END, f"\n[4] SAFE USER RECOMMENDATION:\n")
        self.link_output.insert(tk.END, f"  {report['safe_advice']}\n")

    def _build_payload_tab(self):
        frame = tk.Frame(self.tab_payload, bg="#0f172a", padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Inspect Executable, APK or Suspicious Application Payload:", font=("Segoe UI", 10, "bold"), bg="#0f172a", fg="#94a3b8").pack(anchor="w")

        btn_row = tk.Frame(frame, bg="#0f172a")
        btn_row.pack(fill="x", pady=(6, 12))

        btn_pick = tk.Button(
            btn_row,
            text="📁 Select File from Disk...",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
            bd=1,
            relief="solid",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._select_and_scan_file
        )
        btn_pick.pack(side="left", padx=(0, 8))

        btn_test_apk = tk.Button(
            btn_row,
            text="⚡ Test Bundled Simulated APK (BankSecure_Update.apk)",
            font=("Segoe UI", 10, "bold"),
            bg="#be123c",
            fg="#ffffff",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._test_bundled_apk
        )
        btn_test_apk.pack(side="left")

        self.payload_output = tk.Text(frame, bg="#1e293b", fg="#f8fafc", font=("Consolas", 10), padx=10, pady=10, bd=1, relief="solid")
        self.payload_output.pack(fill="both", expand=True)

        # Pre-fill with description
        self.payload_output.insert(tk.END, "Click 'Test Bundled Simulated APK' or select any file to inspect for sideloading and dropper risks.\n")

    def _select_and_scan_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self._scan_filepath(filepath)

    def _test_bundled_apk(self):
        # Create safe test APK if it doesn't exist
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_payloads")
        os.makedirs(test_dir, exist_ok=True)
        apk_path = os.path.join(test_dir, "BankSecure_Update.apk")
        if not os.path.exists(apk_path):
            with open(apk_path, "wb") as f:
                f.write(b"SENTINX-SIMULATED-MALWARE-TEST-PAYLOAD-NOT-HARMFUL")
        self._scan_filepath(apk_path)

    def _scan_filepath(self, filepath):
        filename = os.path.basename(filepath)
        size_bytes = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        ext = os.path.splitext(filename)[1].lower()

        sha256 = ""
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()

        danger_info = self.link_guard.dangerous_extensions.get(ext)

        self.payload_output.delete("1.0", tk.END)
        self.payload_output.insert(tk.END, f"=========================================================================\n")
        self.payload_output.insert(tk.END, f"  PAYLOAD & APPLICATION SECURITY SCAN REPORT\n")
        self.payload_output.insert(tk.END, f"=========================================================================\n\n")
        self.payload_output.insert(tk.END, f"FILE NAME:       {filename}\n")
        self.payload_output.insert(tk.END, f"FILE SIZE:       {size_bytes} bytes\n")
        self.payload_output.insert(tk.END, f"SHA-256 HASH:    {sha256}\n\n")

        if danger_info:
            app_name, desc = danger_info
            self.payload_output.insert(tk.END, f"VERDICT:         🚨 BLOCKED: HIGH-RISK EXECUTABLE PAYLOAD\n")
            self.payload_output.insert(tk.END, f"CLASSIFICATION:  {app_name} ({ext})\n")
            self.payload_output.insert(tk.END, f"DANGER LEVEL:    CRITICAL (Direct Sideloading / Binary Execution Risk)\n\n")
            self.payload_output.insert(tk.END, f"[SECURITY RISK DESCRIPTION]:\n")
            self.payload_output.insert(tk.END, f"  {desc}\n\n")
            self.payload_output.insert(tk.END, f"[RECOMMENDED ACTION]:\n")
            self.payload_output.insert(tk.END, f"  Do not install or open this application outside official app stores (Google Play / App Store).\n")
            self.payload_output.insert(tk.END, f"  Sideloaded APKs frequently contain banking trojans, keyloggers, and SMS interceptors.\n")
        else:
            self.payload_output.insert(tk.END, f"VERDICT:         ✅ BENIGN FILE EXTENSION ({ext})\n")
            self.payload_output.insert(tk.END, f"No dangerous executable application extensions detected.\n")

    def _build_footer(self):
        footer = tk.Frame(self.root, bg="#0f172a", height=30, padx=14, pady=6)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="SentinX Desktop Client • Standalone Zero-Trust Security Gateway Engine",
            font=("Segoe UI", 8),
            bg="#0f172a",
            fg="#64748b"
        ).pack(side="left")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinXDesktopTestApp(root)
    root.mainloop()
