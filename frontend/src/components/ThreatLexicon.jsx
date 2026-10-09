import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Search, ShieldAlert, Link2, Globe, 
  Tag, Filter, AlertTriangle, CheckCircle, Database 
} from 'lucide-react';
import { getThreatLexicon } from '../api';

export default function ThreatLexicon() {
  const [lexicon, setLexicon] = useState(null);
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState('nlp'); // 'nlp', 'links', 'brands_tlds'
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLexicon();
  }, []);

  async function loadLexicon() {
    setLoading(true);
    try {
      const data = await getThreatLexicon();
      setLexicon(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  const filteredNlp = lexicon?.nlp_categories.filter((cat) => {
    if (!search) return true;
    const q = search.toLowerCase();
    const matchLabel = cat.label.toLowerCase().includes(q);
    const matchDesc = cat.description.toLowerCase().includes(q);
    const matchKw = cat.keywords.some((k) => k.toLowerCase().includes(q));
    return matchLabel || matchDesc || matchKw;
  }) || [];

  const filteredLinks = lexicon?.url_categories.filter((cat) => {
    if (!search) return true;
    const q = search.toLowerCase();
    const matchLabel = cat.label.toLowerCase().includes(q);
    const matchToken = cat.tokens.some((t) => t.toLowerCase().includes(q));
    return matchLabel || matchToken;
  }) || [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-purple-950/30 to-slate-900 border border-purple-900/40 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 bg-purple-500/20 text-purple-400 rounded-xl border border-purple-500/30">
              <Database className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                Threat Intelligence & Fraud Lexicon
                <span className="text-xs px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 font-mono">
                  150+ Monitored Keywords & Link Tokens
                </span>
              </h2>
              <p className="text-sm text-slate-300 mt-1 max-w-3xl">
                The engine continuously evaluates messages and links against modern fraud vectors—including 
                <strong> KYC expiry, electricity power threats, YouTube task scams, instant loan traps, and deceptive URL tokens</strong>.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Search & Navigation Bar */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Search Bar */}
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search keywords (e.g. kyc, electricity, lottery, login, pan)..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-2 text-slate-500 hover:text-slate-300 text-xs"
            >
              Clear
            </button>
          )}
        </div>

        {/* View Switcher */}
        <div className="flex items-center space-x-1 bg-slate-950 p-1 rounded-xl border border-slate-800 w-full sm:w-auto">
          <button
            onClick={() => setActiveTab('nlp')}
            className={`flex-1 sm:flex-none px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer ${
              activeTab === 'nlp'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Message & Fraud Patterns ({filteredNlp.length})
          </button>
          <button
            onClick={() => setActiveTab('links')}
            className={`flex-1 sm:flex-none px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer ${
              activeTab === 'links'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            URL & Link Tokens ({filteredLinks.length})
          </button>
          <button
            onClick={() => setActiveTab('brands_tlds')}
            className={`flex-1 sm:flex-none px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer ${
              activeTab === 'brands_tlds'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Monitored Brands & Abusive TLDs
          </button>
        </div>
      </div>

      {/* TAB 1: NLP & Semantic Fraud Categories */}
      {activeTab === 'nlp' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredNlp.map((cat) => (
            <div
              key={cat.id}
              className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between shadow-sm hover:border-slate-700 transition"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="text-sm font-semibold text-slate-100">{cat.label}</h3>
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 shrink-0">
                    Weight: +{cat.base_weight}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">{cat.description}</p>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 font-mono uppercase block mb-1.5">Monitored Keywords & Triggers:</span>
                <div className="flex flex-wrap gap-1">
                  {cat.keywords.map((kw, idx) => {
                    const isMatched = search && kw.toLowerCase().includes(search.toLowerCase());
                    return (
                      <span
                        key={idx}
                        className={`text-[10px] px-2 py-0.5 rounded-lg font-mono ${
                          isMatched
                            ? 'bg-cyan-500/30 text-cyan-200 border border-cyan-400'
                            : 'bg-slate-950 text-slate-300 border border-slate-800'
                        }`}
                      >
                        {kw}
                      </span>
                    );
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 2: URL & Link Fraud Tokens */}
      {activeTab === 'links' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredLinks.map((cat, idx) => (
            <div
              key={idx}
              className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between shadow-sm hover:border-slate-700 transition"
            >
              <div>
                <div className="flex items-center space-x-2 text-cyan-400 mb-2">
                  <Link2 className="w-4 h-4" />
                  <h3 className="text-sm font-semibold text-slate-100">{cat.label}</h3>
                </div>
                <p className="text-xs text-slate-400 mb-3">
                  Scanned across link hostnames, subdomains, URL paths, and query string parameters.
                </p>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 font-mono uppercase block mb-1.5">Monitored URL Tokens:</span>
                <div className="flex flex-wrap gap-1">
                  {cat.tokens.map((token, tIdx) => {
                    const isMatched = search && token.toLowerCase().includes(search.toLowerCase());
                    return (
                      <span
                        key={tIdx}
                        className={`text-[10px] px-2 py-0.5 rounded-lg font-mono ${
                          isMatched
                            ? 'bg-cyan-500/30 text-cyan-200 border border-cyan-400'
                            : 'bg-slate-950 text-slate-300 border border-slate-800'
                        }`}
                      >
                        {token}
                      </span>
                    );
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 3: Monitored Brands & Abusive TLDs */}
      {activeTab === 'brands_tlds' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Monitored Brands */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-cyan-400" />
              Monitored Brands (Subdomain Spoofing & Lookalike Defense)
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              If an unverified domain contains any of these brand names (or embeds them in subdomains like <code>paypal.com.attacker.xyz</code>), the link is immediately flagged for brand hijacking.
            </p>
            <div className="flex flex-wrap gap-1.5 pt-2">
              {lexicon?.monitored_brands.map((brand, idx) => (
                <span key={idx} className="text-xs px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-200 font-mono">
                  {brand}
                </span>
              ))}
            </div>
          </div>

          {/* Abusive TLDs */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Globe className="w-4 h-4 text-rose-400" />
              High-Risk / Abusive Top-Level Domains (TLDs)
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Cheap or disposable domain extensions frequently purchased in bulk by cybercriminal syndicates for transient phishing operations.
            </p>
            <div className="flex flex-wrap gap-1.5 pt-2">
              {lexicon?.risky_tlds.map((tld, idx) => (
                <span key={idx} className="text-xs px-2.5 py-1 rounded-lg bg-rose-950/40 border border-rose-500/30 text-rose-300 font-mono">
                  .{tld}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
