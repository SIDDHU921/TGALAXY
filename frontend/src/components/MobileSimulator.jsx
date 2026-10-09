import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, ShieldCheck, AlertTriangle, Smartphone, Send, 
  ExternalLink, UserCheck, UserX, AlertOctagon, Info, RefreshCw, 
  FileWarning, Lock, ChevronRight, Zap
} from 'lucide-react';
import { checkMessage, getScenarios } from '../api';

export default function MobileSimulator({ onAssessmentDone }) {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Custom message input state
  const [sender, setSender] = useState('+1 (917) 555-0199');
  const [senderName, setSenderName] = useState('Walmart Rewards');
  const [channel, setChannel] = useState('SMS');
  const [content, setContent] = useState('CONGRATULATIONS! You have been selected as our Walmart $1,000 gift card winner. Claim your prize now at http://walmart-winner-card.xyz before it expires in 12 hours!');
  
  // Active Assessment Result
  const [assessment, setAssessment] = useState(null);
  const [linkModalUrl, setLinkModalUrl] = useState(null);
  const [revealedInPhone, setRevealedInPhone] = useState(false);

  useEffect(() => {
    loadScenarios();
  }, []);

  async function loadScenarios() {
    try {
      const data = await getScenarios();
      setScenarios(data);
      if (data.length > 0) {
        setSelectedScenarioId(data[0].id);
        applyScenario(data[0]);
      }
    } catch (err) {
      console.error(err);
    }
  }

  function applyScenario(scen) {
    setSelectedScenarioId(scen.id);
    setSender(scen.sender);
    setSenderName(scen.sender_name);
    setChannel(scen.channel);
    setContent(scen.content);
    setRevealedInPhone(false);
    runInspection({
      sender: scen.sender,
      sender_name: scen.sender_name,
      channel: scen.channel,
      content: scen.content
    });
  }

  async function runInspection(payload) {
    setLoading(true);
    try {
      const result = await checkMessage(payload);
      setAssessment(result);
      if (onAssessmentDone) onAssessmentDone(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    setRevealedInPhone(false);
    runInspection({ sender, sender_name: senderName, channel, content });
  }

  // Intercept click on links in simulated message
  function handleSimulatedLinkClick(url) {
    setLinkModalUrl(url);
  }

  // Render clickable links inside text message
  function renderFormattedMessage(text) {
    const urlRegex = /(https?:\/\/[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(?:com|org|net|xyz|top|site|link|click|app)\b[^\s]*)/gi;
    const parts = text.split(urlRegex);

    return parts.map((part, idx) => {
      if (part.match(urlRegex)) {
        return (
          <button
            key={idx}
            type="button"
            onClick={() => handleSimulatedLinkClick(part)}
            className="text-cyan-400 underline font-mono hover:text-cyan-300 break-all inline-flex items-center space-x-1 cursor-pointer bg-cyan-950/40 px-1 py-0.5 rounded"
          >
            <span>{part}</span>
            <ExternalLink className="w-3 h-3 ml-0.5 inline opacity-70" />
          </button>
        );
      }
      return <span key={idx}>{part}</span>;
    });
  }

  return (
    <div className="space-y-6">
      {/* Top Banner explaining the Pre-Interaction Concept */}
      <div className="bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-cyan-800/40 rounded-2xl p-5 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 bg-cyan-500/20 text-cyan-400 rounded-xl border border-cyan-500/30">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                Pre-Interaction Interception & Virtual Shield
                <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-mono">
                  Slide 4 & 7 Architecture
                </span>
              </h2>
              <p className="text-sm text-slate-300 mt-1 max-w-3xl">
                Unlike traditional apps that only block phone numbers after the user is disturbed, our security layer inspects 
                <strong> Sender Trust (Contacts), Intent NLP, Pre-Click Links, and APK Payloads BEFORE the user opens or interacts</strong>.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-950/60 px-3 py-2 rounded-lg border border-slate-800 shrink-0">
            <Lock className="w-4 h-4 text-cyan-400" />
            <span>Zero-Trust Inspection Pipeline</span>
          </div>
        </div>
      </div>

      {/* Main 3-Column Interactive Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: Scenario Quick-Selector & Custom Message Form */}
        <div className="lg:col-span-4 space-y-5">
          {/* Quick Attack & Test Scenarios */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Smartphone className="w-3.5 h-3.5 text-cyan-400" />
                1-Click Threat Scenarios
              </span>
              <span className="text-[11px] text-slate-500">Preset Demonstrations</span>
            </div>
            
            <div className="space-y-2">
              {scenarios.map((scen) => {
                const isSelected = selectedScenarioId === scen.id;
                const isBlock = scen.expected_disposition === 'BLOCK';
                return (
                  <button
                    key={scen.id}
                    onClick={() => applyScenario(scen)}
                    className={`w-full text-left p-2.5 rounded-xl text-xs transition-all border ${
                      isSelected
                        ? 'bg-cyan-950/60 border-cyan-500/50 shadow-sm shadow-cyan-500/10'
                        : 'bg-slate-950/40 border-slate-800/80 hover:bg-slate-800/50 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-slate-200">{scen.title}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                        isBlock 
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' 
                          : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      }`}>
                        {scen.expected_disposition}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1 line-clamp-1">{scen.description}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Custom Message Inspector Form */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-sm">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-3">
              Custom Message Test Sandbox
            </span>
            <form onSubmit={handleSubmit} className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] text-slate-400 block mb-1">Channel</label>
                  <select
                    value={channel}
                    onChange={(e) => setChannel(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
                  >
                    <option value="SMS">SMS</option>
                    <option value="WhatsApp">WhatsApp</option>
                    <option value="Telegram">Telegram</option>
                    <option value="Email">Email</option>
                    <option value="Social">Social DM</option>
                  </select>
                </div>
                <div>
                  <label className="text-[11px] text-slate-400 block mb-1">Sender Identifier</label>
                  <input
                    type="text"
                    value={sender}
                    onChange={(e) => setSender(e.target.value)}
                    placeholder="+1 (555) 000-0000"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Display Name (Claimed Identity)</label>
                <input
                  type="text"
                  value={senderName}
                  onChange={(e) => setSenderName(e.target.value)}
                  placeholder="e.g. Amazon Support, Chase Alert, Sister"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Message Text (Include links or .apk mentions)</label>
                <textarea
                  rows={4}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Type or paste incoming message..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 px-4 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 flex items-center justify-center space-x-2 transition-all cursor-pointer"
              >
                {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
                <span>Trigger Pre-Interaction Interception</span>
              </button>
            </form>
          </div>
        </div>

        {/* MIDDLE COLUMN: Interactive Smartphone Guard Device Frame */}
        <div className="lg:col-span-4 flex justify-center">
          <div className="w-[320px] sm:w-[350px] bg-slate-950 border-4 border-slate-800 rounded-[42px] p-3.5 shadow-2xl shadow-cyan-950/30 flex flex-col relative overflow-hidden ring-1 ring-slate-700/50">
            {/* Phone Top Notch / Dynamic Island */}
            <div className="flex items-center justify-between px-4 pt-1 pb-2">
              <span className="text-[11px] font-semibold text-slate-400 font-mono">9:41</span>
              <div className="w-20 h-4 bg-slate-900 rounded-full border border-slate-800 flex items-center justify-center">
                <div className="w-2 h-2 rounded-full bg-slate-950"></div>
              </div>
              <div className="flex items-center space-x-1 text-[10px] text-slate-400 font-mono">
                <span>5G</span>
                <span>100%</span>
              </div>
            </div>

            {/* App Header Inside Phone */}
            <div className="bg-slate-900/90 rounded-2xl p-2.5 mb-3 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-7 h-7 rounded-full bg-cyan-600 flex items-center justify-center text-white font-bold text-xs">
                  {senderName ? senderName[0].toUpperCase() : 'U'}
                </div>
                <div>
                  <div className="text-xs font-semibold text-slate-100 flex items-center gap-1">
                    <span>{senderName || sender}</span>
                    {assessment?.is_known_contact ? (
                      <span title="Verified in Address Book">
                        <UserCheck className="w-3 h-3 text-emerald-400 inline" />
                      </span>
                    ) : (
                      <span title="Unknown Sender">
                        <UserX className="w-3 h-3 text-amber-400 inline" />
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">{channel} • {sender}</span>
                </div>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-medium">
                {channel}
              </span>
            </div>

            {/* Real-Time Security Layer Status Indicator in Phone */}
            {assessment && (
              <div className={`mb-3 p-2 rounded-xl border text-[11px] flex items-center justify-between transition-all ${
                assessment.disposition === 'BLOCK'
                  ? 'bg-rose-950/60 border-rose-500/40 text-rose-300'
                  : assessment.disposition === 'WARN'
                  ? 'bg-amber-950/60 border-amber-500/40 text-amber-300'
                  : 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300'
              }`}>
                <div className="flex items-center space-x-1.5">
                  {assessment.disposition === 'BLOCK' && <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" />}
                  {assessment.disposition === 'WARN' && <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />}
                  {assessment.disposition === 'SAFE' && <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />}
                  <span className="font-semibold">{assessment.disposition} Dispatched</span>
                </div>
                <span className="font-mono text-[10px]">Score: {assessment.overall_score}/100</span>
              </div>
            )}

            {/* Phone Message Display Area */}
            <div className="flex-1 min-h-[360px] bg-slate-900/40 rounded-2xl p-3 border border-slate-900 flex flex-col justify-end space-y-3 relative overflow-hidden">
              
              {/* If BLOCKED: Show the Pre-Interaction Interception Shield Overlay! */}
              {assessment?.disposition === 'BLOCK' && !revealedInPhone && (
                <div className="absolute inset-0 z-20 bg-slate-950/95 backdrop-blur-md p-4 flex flex-col items-center justify-center text-center rounded-2xl border-2 border-rose-500/50 animate-in fade-in zoom-in-95 duration-200">
                  <div className="w-14 h-14 rounded-2xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400 mb-3 shadow-lg shadow-rose-950/50">
                    <AlertOctagon className="w-8 h-8 animate-pulse" />
                  </div>
                  <span className="text-[11px] font-mono uppercase tracking-wider text-rose-400 font-bold">
                    Pre-Interaction Interception Active
                  </span>
                  <h3 className="text-sm font-bold text-white mt-1">High-Risk Threat Blocked</h3>
                  <p className="text-[11px] text-slate-300 mt-2 leading-relaxed">
                    SentinX Security Layer intercepted this message <strong>before you opened it</strong>. 
                    Deceptive cues, dangerous links, or malicious APKs were flagged.
                  </p>
                  
                  <div className="w-full bg-rose-950/40 border border-rose-500/30 rounded-xl p-2.5 mt-3 text-left">
                    <span className="text-[10px] text-rose-300 font-semibold block uppercase">Safe Recommendation:</span>
                    <p className="text-[11px] text-slate-200 mt-0.5">{assessment.recommendation}</p>
                  </div>

                  <div className="mt-4 flex flex-col w-full gap-2">
                    <button
                      onClick={() => setRevealedInPhone(true)}
                      className="w-full py-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-medium border border-slate-700 cursor-pointer"
                    >
                      Inspect Quarantined Text Anyway
                    </button>
                  </div>
                </div>
              )}

              {/* Message Bubble (Simulated incoming message) */}
              <div className="max-w-[90%] bg-slate-800/90 text-slate-100 rounded-2xl rounded-bl-sm p-3 border border-slate-700/60 shadow-md">
                {/* Advisory Tag above message if WARN */}
                {assessment?.disposition === 'WARN' && (
                  <div className="mb-2 p-1.5 rounded-lg bg-amber-500/20 border border-amber-500/30 text-amber-300 text-[10px] flex items-center gap-1">
                    <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                    <span>Warning: Unverified sender & promotional urgency</span>
                  </div>
                )}

                {/* Advisory Tag if BLOCKED and revealed */}
                {assessment?.disposition === 'BLOCK' && revealedInPhone && (
                  <div className="mb-2 p-1.5 rounded-lg bg-rose-500/20 border border-rose-500/30 text-rose-300 text-[10px] flex items-center justify-between">
                    <div className="flex items-center gap-1">
                      <ShieldAlert className="w-3.5 h-3.5 shrink-0" />
                      <span>Quarantined Payload</span>
                    </div>
                    <button 
                      onClick={() => setRevealedInPhone(false)}
                      className="text-[9px] underline text-rose-400"
                    >
                      Hide
                    </button>
                  </div>
                )}

                {/* Message Body */}
                <div className="text-xs leading-relaxed">
                  {renderFormattedMessage(content)}
                </div>

                <div className="flex items-center justify-between mt-2 pt-1 border-t border-slate-700/40 text-[10px] text-slate-400 font-mono">
                  <span>Now</span>
                  <span>Delivered via {channel}</span>
                </div>
              </div>
            </div>

            {/* Phone Bottom Home Bar */}
            <div className="pt-3 pb-1 flex justify-center">
              <div className="w-28 h-1 bg-slate-700 rounded-full"></div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Real-Time Forensic Report & Safe Suggestion */}
        <div className="lg:col-span-4 space-y-5">
          {assessment ? (
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-cyan-400" />
                  Forensic Threat Analysis
                </span>
                <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold font-mono ${
                  assessment.disposition === 'BLOCK'
                    ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                    : assessment.disposition === 'WARN'
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                }`}>
                  {assessment.disposition}
                </span>
              </div>

              {/* Threat Meter Visual */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-slate-300 font-medium">Aggregated Threat Score</span>
                  <span className="font-mono font-bold text-slate-100">{assessment.overall_score} / 100</span>
                </div>
                <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden border border-slate-800 flex">
                  <div 
                    className={`h-full transition-all duration-500 ${
                      assessment.overall_score >= 75
                        ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                        : assessment.overall_score >= 35
                        ? 'bg-gradient-to-r from-cyan-500 to-amber-500'
                        : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.max(assessment.overall_score, 4)}%` }}
                  ></div>
                </div>
                <p className="text-[11px] text-slate-400 mt-1.5">{assessment.summary}</p>
              </div>

              {/* 4-Layer Security Breakdown */}
              <div className="space-y-2 pt-2 border-t border-slate-800/80">
                <span className="text-[11px] text-slate-400 font-semibold block">Layer Breakdown:</span>
                
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {/* Layer 1: Sender */}
                  <div className="p-2 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <div className="text-[10px] text-slate-400">Layer 1: Sender Trust</div>
                    <div className="font-semibold text-slate-200 mt-0.5 flex items-center justify-between">
                      <span>{assessment.is_known_contact ? 'Known Contact' : 'Unknown Sender'}</span>
                      <span className="font-mono text-cyan-400">{assessment.layer_scores?.sender_risk ?? 0}%</span>
                    </div>
                  </div>

                  {/* Layer 2: NLP */}
                  <div className="p-2 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <div className="text-[10px] text-slate-400">Layer 2: Intent NLP</div>
                    <div className="font-semibold text-slate-200 mt-0.5 flex items-center justify-between">
                      <span>{assessment.layer_scores?.content_risk > 30 ? 'Social Eng.' : 'Neutral'}</span>
                      <span className="font-mono text-cyan-400">{assessment.layer_scores?.content_risk ?? 0}%</span>
                    </div>
                  </div>

                  {/* Layer 3: Link */}
                  <div className="p-2 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <div className="text-[10px] text-slate-400">Layer 3: Pre-Click Link</div>
                    <div className="font-semibold text-slate-200 mt-0.5 flex items-center justify-between">
                      <span>{assessment.extracted_links.length > 0 ? `${assessment.extracted_links.length} Link(s)` : 'None'}</span>
                      <span className="font-mono text-cyan-400">{assessment.layer_scores?.link_risk ?? 0}%</span>
                    </div>
                  </div>

                  {/* Layer 4: Payload / App */}
                  <div className="p-2 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <div className="text-[10px] text-slate-400">Layer 4: App Payload</div>
                    <div className="font-semibold text-slate-200 mt-0.5 flex items-center justify-between">
                      <span>{assessment.extracted_apps.length > 0 ? 'APK/File Dropper' : 'None'}</span>
                      <span className="font-mono text-cyan-400">{assessment.layer_scores?.app_risk ?? 0}%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Safe Suggestion Box (Slide 7 requirement) */}
              <div className="bg-cyan-950/30 border border-cyan-500/30 rounded-xl p-3">
                <span className="text-[11px] font-semibold text-cyan-300 uppercase tracking-wider flex items-center gap-1">
                  <Info className="w-3.5 h-3.5" />
                  Safe User Recommendation
                </span>
                <p className="text-xs text-slate-200 mt-1 leading-relaxed">
                  {assessment.recommendation}
                </p>
              </div>

              {/* Triggered Indicators of Compromise (IOCs) */}
              {assessment.indicators.length > 0 && (
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-[11px] text-slate-400 font-semibold block mb-2">Flagged Indicators:</span>
                  <div className="space-y-1.5 max-h-44 overflow-y-auto pr-1">
                    {assessment.indicators.map((ind, i) => (
                      <div key={i} className="text-[11px] p-2 rounded-lg bg-slate-950/80 border border-slate-800 flex items-start space-x-2">
                        <span className={`px-1.5 py-0.5 rounded text-[9px] font-mono font-bold shrink-0 mt-0.5 ${
                          ind.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' :
                          ind.severity === 'HIGH' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' :
                          ind.severity === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40' :
                          'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                        }`}>
                          {ind.severity}
                        </span>
                        <div>
                          <div className="font-medium text-slate-200">{ind.description}</div>
                          {ind.detail && <div className="text-[10px] text-slate-400 mt-0.5">{ind.detail}</div>}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-64 rounded-2xl border border-dashed border-slate-800 flex flex-col items-center justify-center text-slate-500 text-xs text-center p-4">
              <ShieldAlert className="w-8 h-8 text-slate-600 mb-2" />
              <span>Select or trigger a scenario to view real-time forensic telemetry</span>
            </div>
          )}
        </div>
      </div>

      {/* POPUP MODAL: Pre-Click Link Guard Interception Modal (Simulated when clicking link) */}
      {linkModalUrl && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border-2 border-rose-500/60 rounded-2xl max-w-md w-full p-6 shadow-2xl shadow-rose-950/60 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center space-x-3 text-rose-400 mb-4">
              <div className="p-2.5 rounded-xl bg-rose-500/20 border border-rose-500/40">
                <AlertOctagon className="w-7 h-7" />
              </div>
              <div>
                <h3 className="font-bold text-white text-base">Pre-Click Navigation Intercepted!</h3>
                <span className="text-xs text-rose-300 font-mono">SentinX Link Guard Active (Slide 7)</span>
              </div>
            </div>

            <p className="text-xs text-slate-300 mb-3">
              The security layer intercepted your click <strong>before opening the browser</strong>. 
              The requested URL was analyzed in the security sandbox:
            </p>

            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 font-mono text-xs text-amber-300 break-all mb-4">
              {linkModalUrl}
            </div>

            <div className="bg-rose-950/40 border border-rose-500/30 rounded-xl p-3 mb-4">
              <span className="text-[11px] font-bold text-rose-300 uppercase tracking-wider block mb-1">
                Risk Warning & Recommendation:
              </span>
              <p className="text-xs text-slate-200 leading-relaxed">
                {assessment?.extracted_links?.[0]?.safe_destination_advice || 
                 "This URL exhibits indicators of domain spoofing, suspicious TLDs, or direct unverified payload downloads. Navigation was halted to protect against credential theft and malware."}
              </p>
            </div>

            <div className="flex items-center justify-end space-x-2">
              <button
                type="button"
                onClick={() => setLinkModalUrl(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 cursor-pointer"
              >
                Close & Remain Safe
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
