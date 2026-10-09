import React, { useState } from 'react';
import { 
  Link2, ShieldCheck, ShieldAlert, AlertTriangle, Search, 
  ExternalLink, Info, CheckCircle2, XCircle, ArrowRight, 
  Layers, Code2, AlertOctagon, Zap, Shield, HelpCircle
} from 'lucide-react';
import { analyzeDeepLink } from '../api';

export default function LinkInspector() {
  const [url, setUrl] = useState('https://paypal.com.account-update.xyz/login/verify-kyc?ref=telegram');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  const presets = [
    { label: 'Safari PrizePool Lure (win.prizepool)', url: 'https://win.prizepool.safari.money.com/' },
    { label: 'Subdomain PayPal Hijack', url: 'https://paypal.com.account-update.xyz/login/verify-kyc?ref=telegram' },
    { label: 'Malicious APK Dropper', url: 'http://192.168.1.10/BankSecure_Update.apk?download=instant' },
    { label: 'Chase Phish Credential Harvester', url: 'https://chase-security-update.click/auth/session/login?cmd=_login' },
    { label: 'Electricity Bill Extortion', url: 'https://power-bill-payment.online/electricity/pay-bill?consumer=99281' },
    { label: 'Reward Points Cash Phish', url: 'https://card-rewards-redeem-cash.top/gift/claim-reward?points=450' },
    { label: 'Legitimate Google Docs', url: 'https://google.com/docs/presentation' },
  ];

  async function handleDissect(targetUrl) {
    const toScan = targetUrl || url;
    if (!toScan.trim()) return;
    setLoading(true);
    try {
      const data = await analyzeDeepLink(toScan);
      setReport(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Concept Header */}
      <div className="bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-cyan-800/40 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 bg-cyan-500/20 text-cyan-400 rounded-xl border border-cyan-500/30">
              <Layers className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                Deep Forensic URL & Link Keyword Analyzer
                <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-mono">
                  Full Anatomy & Token Dissection
                </span>
              </h2>
              <p className="text-sm text-slate-300 mt-1 max-w-3xl">
                Deconstructs any link into its raw anatomical segments (Scheme, Subdomains, Host, TLD, Path, and Query parameters) 
                and evaluates every single keyword against <strong>200+ specialized fraud & scam tokens</strong>.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Input & Preset Controls */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row gap-2">
          <div className="relative flex-1">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste any link to analyze every keyword token..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono pr-12"
            />
            {url && (
              <button
                type="button"
                onClick={() => setUrl('')}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300 text-xs"
              >
                Clear
              </button>
            )}
          </div>
          <button
            onClick={() => handleDissect()}
            disabled={loading}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 flex items-center justify-center space-x-2 transition cursor-pointer"
          >
            <Search className="w-4 h-4" />
            <span>{loading ? 'Dissecting Link...' : 'Dissect & Analyze All Keywords'}</span>
          </button>
        </div>

        {/* 1-Click Forensic Scenarios */}
        <div className="mt-4 flex flex-wrap items-center gap-1.5 text-xs">
          <span className="text-slate-500 text-[11px] mr-1 font-semibold uppercase">Real-World Scam Links:</span>
          {presets.map((p, idx) => (
            <button
              key={idx}
              onClick={() => {
                setUrl(p.url);
                handleDissect(p.url);
              }}
              className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 hover:border-cyan-500/50 text-slate-300 hover:text-cyan-300 text-[11px] transition cursor-pointer"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Forensic Report Output */}
      {report && (
        <div className="space-y-6">
          {/* Top Verdict Bar */}
          <div className={`p-5 rounded-2xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
            report.composite_risk_score >= 70
              ? 'bg-rose-950/40 border-rose-500/40 text-rose-200'
              : report.composite_risk_score >= 35
              ? 'bg-amber-950/40 border-amber-500/40 text-amber-200'
              : 'bg-emerald-950/40 border-emerald-500/40 text-emerald-200'
          }`}>
            <div className="flex items-center space-x-3">
              <div className={`p-3 rounded-xl ${
                report.composite_risk_score >= 70 ? 'bg-rose-500/20 text-rose-400' :
                report.composite_risk_score >= 35 ? 'bg-amber-500/20 text-amber-400' :
                'bg-emerald-500/20 text-emerald-400'
              }`}>
                {report.composite_risk_score >= 70 ? <AlertOctagon className="w-7 h-7" /> :
                 report.composite_risk_score >= 35 ? <AlertTriangle className="w-7 h-7" /> :
                 <ShieldCheck className="w-7 h-7" />}
              </div>
              <div>
                <span className="text-xs font-mono font-bold uppercase tracking-wider block">
                  {report.verdict_badge}
                </span>
                <h3 className="text-base font-bold text-white mt-0.5 font-mono break-all">
                  {report.normalized_url}
                </h3>
              </div>
            </div>

            <div className="text-right shrink-0">
              <span className="text-[10px] text-slate-400 font-mono uppercase block">Aggregated Link Threat</span>
              <span className={`text-2xl font-bold font-mono ${
                report.composite_risk_score >= 70 ? 'text-rose-400' :
                report.composite_risk_score >= 35 ? 'text-amber-400' : 'text-emerald-400'
              }`}>
                {report.composite_risk_score} / 100
              </span>
            </div>
          </div>

          {/* Safe Recommendation Box */}
          <div className="bg-cyan-950/30 border border-cyan-500/30 rounded-2xl p-4">
            <span className="text-xs font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5 mb-1">
              <Info className="w-4 h-4" />
              Pre-Click Advisory & Safe Recommendation (Slide 7):
            </span>
            <p className="text-xs text-slate-200 leading-relaxed font-sans">
              {report.safe_advice}
            </p>
          </div>

          {/* 1. VISUAL URL ANATOMY BREAKDOWN */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Code2 className="w-4 h-4 text-cyan-400" />
                Visual URL Anatomy & Segment Breakdown
              </h4>
              <span className="text-[11px] text-slate-500 font-mono">Structural Dissection</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2 text-xs font-mono">
              {/* Scheme */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 block uppercase font-sans">Protocol</span>
                <span className="text-slate-200 font-semibold">{report.anatomy.scheme}://</span>
              </div>

              {/* Subdomains */}
              <div className={`p-3 bg-slate-950 rounded-xl border ${
                report.anatomy.subdomains.length > 0 ? 'border-amber-500/30' : 'border-slate-800'
              }`}>
                <div className="flex justify-between items-center text-[10px] text-slate-500 uppercase font-sans">
                  <span>Subdomain(s)</span>
                  {report.anatomy.subdomains.length > 1 && (
                    <span className="text-amber-400 font-mono">{report.anatomy.subdomains.length} Chained</span>
                  )}
                </div>
                <span className="text-amber-300 font-semibold break-all">
                  {report.anatomy.subdomains.length > 0 ? report.anatomy.subdomains.join('.') : '(None)'}
                </span>
              </div>

              {/* Host / Second-Level Domain */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 block uppercase font-sans">Root Domain (SLD)</span>
                <span className="text-cyan-400 font-semibold break-all">{report.anatomy.domain}</span>
              </div>

              {/* TLD */}
              <div className={`p-3 bg-slate-950 rounded-xl border ${
                report.anatomy.is_abusive_tld ? 'border-rose-500/40 bg-rose-950/20' : 'border-slate-800'
              }`}>
                <div className="flex justify-between items-center text-[10px] text-slate-500 uppercase font-sans">
                  <span>Top-Level Domain</span>
                  {report.anatomy.is_abusive_tld && <span className="text-rose-400 font-mono">High Risk</span>}
                </div>
                <span className={`font-semibold ${report.anatomy.is_abusive_tld ? 'text-rose-400' : 'text-slate-200'}`}>
                  .{report.anatomy.tld}
                </span>
              </div>

              {/* Payload Extension */}
              <div className={`p-3 bg-slate-950 rounded-xl border ${
                report.anatomy.payload_extension ? 'border-rose-500/40 bg-rose-950/20' : 'border-slate-800'
              }`}>
                <span className="text-[10px] text-slate-500 block uppercase font-sans">Payload / Dropper</span>
                <span className={report.anatomy.payload_extension ? 'text-rose-400 font-bold' : 'text-slate-400'}>
                  {report.anatomy.payload_extension || 'No Direct Payload'}
                </span>
              </div>
            </div>

            {/* Path & Query Display */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono pt-1">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 block uppercase font-sans">URL Path Segments:</span>
                <span className="text-slate-200 break-all">{report.anatomy.path || '/'}</span>
              </div>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 block uppercase font-sans">Query String & Tokens:</span>
                <span className="text-slate-200 break-all">
                  {Object.keys(report.anatomy.query_params).length > 0 
                    ? JSON.stringify(report.anatomy.query_params) 
                    : '(None)'}
                </span>
              </div>
            </div>
          </div>

          {/* 2. EVERY DETECTED KEYWORD MATCH MATRIX */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Zap className="w-4 h-4 text-cyan-400" />
                  Detected Fraud & Scam Keywords ({report.total_keywords_detected})
                </h4>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  Every keyword token matched across URL subdomains, path directories, and parameters.
                </p>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                {report.total_keywords_detected} Keyword Matches
              </span>
            </div>

            {report.flagged_keywords.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-xl">
                No deceptive keywords or phishing tokens were found in this URL.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                    <tr>
                      <th className="p-2.5">Keyword Token</th>
                      <th className="p-2.5">Location in Link</th>
                      <th className="p-2.5">Fraud Classification</th>
                      <th className="p-2.5">Severity</th>
                      <th className="p-2.5 text-right">Risk Impact</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {report.flagged_keywords.map((kw, i) => (
                      <tr key={i} className="hover:bg-slate-800/40">
                        <td className="p-2.5 text-cyan-300 font-bold font-mono">
                          <span className="bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
                            {kw.keyword}
                          </span>
                        </td>
                        <td className="p-2.5 text-slate-300 font-sans">
                          <span className="text-[11px] bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                            {kw.location}
                          </span>
                        </td>
                        <td className="p-2.5 text-slate-200 font-sans font-medium">
                          {kw.category_label}
                        </td>
                        <td className="p-2.5">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            kw.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                            kw.severity === 'HIGH' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                            'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30'
                          }`}>
                            {kw.severity}
                          </span>
                        </td>
                        <td className="p-2.5 text-right text-rose-400 font-bold">
                          +{kw.weight}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* 3. STRUCTURAL FORENSIC REASONS */}
          {report.threat_reasons.length > 0 && (
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <AlertOctagon className="w-4 h-4 text-rose-400" />
                Structural Violations & Indicators of Compromise ({report.threat_reasons.length})
              </h4>
              <div className="space-y-1.5">
                {report.threat_reasons.map((r, i) => (
                  <div key={i} className="text-xs p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-start space-x-2">
                    <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    <span className="text-slate-200">{r}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
