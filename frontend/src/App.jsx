import React, { useState } from 'react';
import Navbar from './components/Navbar';
import MobileSimulator from './components/MobileSimulator';
import SocDashboard from './components/SocDashboard';
import LinkInspector from './components/LinkInspector';
import ThreatLexicon from './components/ThreatLexicon';
import ContactsVault from './components/ContactsVault';
import { ShieldCheck, Sparkles, Terminal } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('simulator');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Top Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'simulator' && <MobileSimulator />}
        {activeTab === 'soc' && <SocDashboard />}
        {activeTab === 'link_guard' && <LinkInspector />}
        {activeTab === 'lexicon' && <ThreatLexicon />}
        {activeTab === 'contacts' && <ContactsVault />}
      </main>

      {/* System Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-4 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
            <span>SentinX Smart Spam Detection & Security Layer</span>
            <span className="text-slate-600">|</span>
            <span>Pre-Interaction Interception Architecture</span>
          </div>
          <div className="flex items-center space-x-4 text-[11px] text-slate-400">
            <span>FastAPI Backend :8000</span>
            <span>•</span>
            <span>React Vite Frontend :5173</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
