const API_BASE = '/api';

export async function checkMessage(payload) {
  const res = await fetch(`${API_BASE}/check-message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to inspect message');
  return res.json();
}

export async function checkLink(payload) {
  const res = await fetch(`${API_BASE}/check-link`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to inspect link');
  return res.json();
}

export async function analyzeDeepLink(url) {
  const res = await fetch(`${API_BASE}/deep-link-analysis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  if (!res.ok) throw new Error('Failed to dissect link');
  return res.json();
}

export async function getScenarios() {
  const res = await fetch(`${API_BASE}/scenarios`);
  if (!res.ok) throw new Error('Failed to load test scenarios');
  return res.json();
}

export async function getContacts() {
  const res = await fetch(`${API_BASE}/contacts`);
  if (!res.ok) throw new Error('Failed to load contacts');
  return res.json();
}

export async function addContact(contact) {
  const res = await fetch(`${API_BASE}/contacts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contact)
  });
  if (!res.ok) throw new Error('Failed to add contact');
  return res.json();
}

export async function deleteContact(id) {
  const res = await fetch(`${API_BASE}/contacts/${id}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to delete contact');
  return res.json();
}

export async function getTelemetry() {
  const res = await fetch(`${API_BASE}/telemetry`);
  if (!res.ok) throw new Error('Failed to load telemetry stats');
  return res.json();
}

export async function getThreatHistory() {
  const res = await fetch(`${API_BASE}/threat-history`);
  if (!res.ok) throw new Error('Failed to load threat history');
  return res.json();
}

export async function getThreatLexicon() {
  const res = await fetch(`${API_BASE}/threat-lexicon`);
  if (!res.ok) throw new Error('Failed to load threat lexicon');
  return res.json();
}

export async function resetTelemetry() {
  const res = await fetch(`${API_BASE}/reset-telemetry`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to reset telemetry');
  return res.json();
}
