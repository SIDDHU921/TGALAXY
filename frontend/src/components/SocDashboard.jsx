import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, ShieldAlert, AlertTriangle, Activity, 
  Link2, FileWarning, Gift, UserX, RefreshCw, Trash2 
} from 'lucide-react';
import { getTelemetry, getThreatHistory, resetTelemetry } from '../api';

export default function SocDashboard() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedAudit, setSelectedAudit] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const [tData, hData] = await Promise.all([getTelemetry(), getThreatHistory()]);
      setStats(tData);
      setHistory(hData);
      if (hData.length > 0 && !selectedAudit) {
        setSelectedAudit(hData[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleReset() {
    if (window.confirm("Reset all telemetry counters and history for a new demonstration?")) {
      await resetTelemetry();
      fetchData();
      setSelectedAudit(null);
    }
  }

  const kpis = [
    { label: 'Total Interceptions', value: stats?.total_inspected ?? 0, icon: Activity, color: 'text-cyan-400', border: 'border-cyan-500/30' },
    { label: 'High Threats Blocked', value: stats?.blocked_count ?? 0, icon: ShieldAlert, color: 'text-rose-400', border: 'border-rose-500/30' },
    { label: 'Warnings Issued', value: stats?.warn_count ?? 0, icon: AlertTriangle, color: 'text-amber-400', border: 'border-amber-500/30' },
    { label: 'Verified Safe Passed', value: stats?.safe_count ?? 0, icon: ShieldCheck, color: 'text-emerald-400', border: 'border-emerald-500/30' },
    { label: 'Phishing Links Caught', value: stats?.malicious_links_caught ?? 0, icon: Link2, color: 'text-cyan-400', border: 'border-cyan-500/30' },
    { label: 'Dangerous APKs Deflected', value: stats?.dangerous_apps_stopped ?? 0, icon: FileWarning, color: 'text-rose-400', border: 'border-rose-500/30' },
    { label: 'Fake Offers Intercepted', value: stats?.fake_offers_intercepted ?? 0, icon: Gift, color: 'text-yellow-400', border: 'border-yellow-500/30' },
    { label: 'Impersonations Caught', value: stats?.impersonations_detected ?? 0, icon: UserX, color: 'text-purple-400', border: 'border-purple-500/30' },
  ];

  return (
    <div className="space-y-6">
      {/* Header with Refresh and Reset */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/80 border border-slate-800 rounded-2xl p-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            Security Operations Center (SOC) Telemetry
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time telemetry and threat intelligence aggregated from the pre-interaction gateway.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={fetchData}
            disabled={loading}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 border border-slate-700 transition cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-rose-950/40 hover:bg-rose-900/40 text-rose-300 text-xs border border-rose-800/40 transition cursor-pointer"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Reset Demo</span>
          </button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className={`bg-slate-900/80 border ${kpi.border} rounded-2xl p-4 flex items-center justify-between shadow-sm`}>
              <div>
                <span className="text-xs text-slate-400 block font-medium">{kpi.label}</span>
                <span className={`text-2xl font-bold font-mono mt-1 block ${kpi.color}`}>{kpi.value}</span>
              </div>
              <div className={`p-2.5 rounded-xl bg-slate-950 border border-slate-800 ${kpi.color}`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* History Ledger & Forensic Inspection Details */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* History Table */}
        <div className="lg:col-span-7 bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200">Pre-Interaction Threat Log</h3>
            <span className="text-xs text-slate-500 font-mono">{history.length} events logged</span>
          </div>

          {history.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-xl">
              No messages scanned yet. Run scenarios in the Device Simulator to populate telemetry!
            </div>
          ) : (
            <div className="overflow-x-auto max-h-[420px] overflow-y-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 sticky top-0">
                  <tr>
                    <th className="p-2.5">Time</th>
                    <th className="p-2.5">Channel</th>
                    <th className="p-2.5">Sender</th>
                    <th className="p-2.5">Disposition</th>
                    <th className="p-2.5 text-right">Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {history.map((item) => {
                    const isSelected = selectedAudit?.id === item.id;
                    return (
                      <tr
                        key={item.id}
                        onClick={() => setSelectedAudit(item)}
                        className={`cursor-pointer transition-colors ${
                          isSelected ? 'bg-cyan-950/50' : 'hover:bg-slate-800/40'
                        }`}
                      >
                        <td className="p-2.5 text-slate-400 text-[11px] whitespace-nowrap">{item.timestamp.split(' ')[1]}</td>
                        <td className="p-2.5 text-slate-300">{item.channel}</td>
                        <td className="p-2.5 text-slate-200 truncate max-w-[140px] font-sans">
                          {item.sender_name || item.sender}
                        </td>
                        <td className="p-2.5">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.disposition === 'BLOCK' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                            item.disposition === 'WARN' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                            'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                          }`}>
                            {item.disposition}
                          </span>
                        </td>
                        <td className="p-2.5 text-right font-bold text-slate-200">{item.overall_score}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Selected Audit Item Details */}
        <div className="lg:col-span-5 bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-semibold text-slate-200">Inspection Forensic Details</h3>
            {selectedAudit && (
              <span className="text-[11px] font-mono text-cyan-400">{selectedAudit.id}</span>
            )}
          </div>

          {selectedAudit ? (
            <div className="space-y-4 text-xs">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
                <div className="flex justify-between text-slate-400">
                  <span>Sender Identifier:</span>
                  <span className="font-mono text-slate-200">{selectedAudit.sender}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Claimed Identity:</span>
                  <span className="text-slate-200">{selectedAudit.sender_name || 'None provided'}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Saved in Contacts:</span>
                  <span className={selectedAudit.is_known_contact ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                    {selectedAudit.is_known_contact ? 'Yes (Trusted)' : 'No (Unknown Sender)'}
                  </span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Threat Score:</span>
                  <span className="font-mono font-bold text-rose-400">{selectedAudit.overall_score} / 100</span>
                </div>
              </div>

              <div>
                <span className="text-[11px] text-slate-400 font-semibold block mb-1">System Action:</span>
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-medium text-slate-200">
                  {selectedAudit.action_banner}
                </div>
              </div>

              <div>
                <span className="text-[11px] text-slate-400 font-semibold block mb-1">Actionable Recommendation:</span>
                <div className="p-2.5 rounded-xl bg-cyan-950/30 border border-cyan-800/40 text-slate-200">
                  {selectedAudit.recommendation}
                </div>
              </div>

              {selectedAudit.indicators.length > 0 && (
                <div>
                  <span className="text-[11px] text-slate-400 font-semibold block mb-1.5">Indicators of Compromise:</span>
                  <div className="space-y-1.5 max-h-40 overflow-y-auto">
                    {selectedAudit.indicators.map((ind, i) => (
                      <div key={i} className="p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px]">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-slate-200">{ind.description}</span>
                          <span className="text-[10px] text-cyan-400 font-mono">{ind.layer}</span>
                        </div>
                        {ind.detail && <p className="text-[10px] text-slate-400 mt-0.5">{ind.detail}</p>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="py-12 text-center text-xs text-slate-500">
              Select an item from the threat log to view forensic breakdown
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
