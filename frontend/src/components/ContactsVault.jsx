import React, { useState, useEffect } from 'react';
import { Users, UserPlus, Trash2, ShieldCheck, ShieldAlert, CheckCircle, Info } from 'lucide-react';
import { getContacts, addContact, deleteContact } from '../api';

export default function ContactsVault() {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  // New Contact State
  const [name, setName] = useState('');
  const [identifier, setIdentifier] = useState('');
  const [relationship, setRelationship] = useState('Friend');
  const [trustLevel, setTrustLevel] = useState('TRUSTED');

  useEffect(() => {
    loadContacts();
  }, []);

  async function loadContacts() {
    setLoading(true);
    try {
      const data = await getContacts();
      setContacts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd(e) {
    e.preventDefault();
    if (!name || !identifier) return;
    try {
      await addContact({ name, identifier, relationship, trust_level: trustLevel });
      setName('');
      setIdentifier('');
      setShowAddForm(false);
      loadContacts();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleDelete(id) {
    try {
      await deleteContact(id);
      loadContacts();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="space-y-6">
      {/* Concept Architecture Card */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950/30 to-slate-900 border border-blue-900/40 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 bg-blue-500/20 text-blue-400 rounded-xl border border-blue-500/30">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                Address Book & Trust Graph Engine
                <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30 font-mono">
                  Slide 6 Architecture
                </span>
              </h2>
              <p className="text-sm text-slate-300 mt-1 max-w-3xl">
                By accessing your contacts, the security layer <strong>avoids disturbing trusted friends and family</strong> with false alarms, 
                while applying <strong>Deep Scrutiny Mode</strong> to any message arriving from unknown numbers or handles.
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 transition cursor-pointer shrink-0"
          >
            <UserPlus className="w-4 h-4" />
            <span>{showAddForm ? 'Cancel' : 'Add New Contact'}</span>
          </button>
        </div>
      </div>

      {/* Add Contact Modal / Expandable Card */}
      {showAddForm && (
        <div className="bg-slate-900/90 border border-cyan-500/40 rounded-2xl p-5 shadow-xl animate-in fade-in duration-200">
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <UserPlus className="w-4 h-4 text-cyan-400" />
            Add Trusted Contact to Address Book
          </h3>
          <form onSubmit={handleAdd} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. John Doe"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>
            <div>
              <label className="text-slate-400 block mb-1">Phone / Identifier</label>
              <input
                type="text"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="+1 (555) 999-0000"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                required
              />
            </div>
            <div>
              <label className="text-slate-400 block mb-1">Relationship</label>
              <select
                value={relationship}
                onChange={(e) => setRelationship(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="Family">Family</option>
                <option value="Friend">Friend</option>
                <option value="Colleague">Colleague / Work</option>
                <option value="Verified Service">Verified Service</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full py-2 px-4 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold transition cursor-pointer"
              >
                Save to Trust Graph
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Contacts List Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {contacts.map((contact) => (
          <div
            key={contact.id}
            className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between shadow-sm hover:border-slate-700 transition"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center text-white font-bold text-sm shadow">
                  {contact.name[0].toUpperCase()}
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">{contact.name}</h4>
                  <span className="text-[11px] text-slate-400 block">{contact.relationship}</span>
                </div>
              </div>
              <button
                onClick={() => handleDelete(contact.id)}
                title="Remove Contact"
                className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-slate-800 transition cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300">{contact.identifier}</span>
              <span className="flex items-center space-x-1 text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full text-[10px]">
                <ShieldCheck className="w-3 h-3" />
                <span>{contact.trust_level}</span>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
