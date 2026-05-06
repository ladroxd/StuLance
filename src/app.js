import { createElement } from 'react';
import { createRoot } from 'react-dom/client';
import { CinematicFooter } from './components/CinematicFooter.jsx';
import { FeaturedMissions } from './components/MissionGlassCard.jsx';

// ── Click sound ───────────────────────────────────────────
let _sndCtx = null;

document.addEventListener('mousedown', function () {
  if (!_sndCtx) _sndCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (_sndCtx.state === 'suspended') _sndCtx.resume();
}, { capture: true });

function _playKick() {
  if (!_sndCtx) return;
  const now = _sndCtx.currentTime;
  const osc = _sndCtx.createOscillator();
  const gain = _sndCtx.createGain();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(95, now);
  osc.frequency.exponentialRampToValueAtTime(38, now + 0.09);
  gain.gain.setValueAtTime(0.55, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
  osc.connect(gain);
  gain.connect(_sndCtx.destination);
  osc.start(now);
  osc.stop(now + 0.28);
}

function _playPop() {
  if (!_sndCtx) return;
  const now = _sndCtx.currentTime;
  const osc = _sndCtx.createOscillator();
  const gain = _sndCtx.createGain();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(400, now);
  osc.frequency.exponentialRampToValueAtTime(150, now + 0.12);
  gain.gain.setValueAtTime(0.4, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
  osc.connect(gain);
  gain.connect(_sndCtx.destination);
  osc.start(now);
  osc.stop(now + 0.12);
}

window._playKick = _playKick;
window._playPop = _playPop;

document.addEventListener('click', function (e) {
  const target = e.target;
  if (target.matches('input[type="checkbox"]')) {
    _playPop();
  } else if (target.closest('a, button, [role="button"], .btn, input[type="submit"], input[type="button"], label[for]')) {
    _playKick();
  }
});

// Notification badge polling
async function updateNotifBadge() {
  try {
    const res = await fetch('/notifications/unread-count/');
    const data = await res.json();
    const badge = document.getElementById('notif-badge');
    if (badge) {
      if (data.count > 0) {
        badge.textContent = data.count;
        badge.classList.remove('d-none');
      } else {
        badge.classList.add('d-none');
      }
    }
  } catch (_) {}
}

if (document.getElementById('notif-bell')) {
  updateNotifBadge();
  setInterval(updateNotifBadge, 30000);
}

// ── Featured Missions ────────────────────────────────────
const missionsRoot = document.getElementById('featured-missions-root');
if (missionsRoot) {
  const dataEl = document.getElementById('featured-missions-data');
  const missions = dataEl ? JSON.parse(dataEl.textContent) : [];
  createRoot(missionsRoot).render(createElement(FeaturedMissions, { missions }));
}

// ── Cinematic Footer ─────────────────────────────────────
const footerRoot = document.getElementById('cinematic-footer-root');
if (footerRoot) {
  createRoot(footerRoot).render(createElement(CinematicFooter));
}
