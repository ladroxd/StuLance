import { createElement } from 'react';
import { createRoot } from 'react-dom/client';
import { CinematicFooter } from './components/CinematicFooter.jsx';
import { FeaturedMissions } from './components/MissionGlassCard.jsx';

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
