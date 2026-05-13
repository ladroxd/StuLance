import { createElement } from 'react';


import { createRoot } from 'react-dom/client';
import { CinematicFooter } from './components/CinematicFooter.jsx';
import { FeaturedMissions } from './components/MissionGlassCard.jsx';


// ── Featured Missions (home page) ────────────────────────
try {
  const missionsRoot = document.getElementById('featured-missions-root');
  if (missionsRoot) {
    const dataEl = document.getElementById('featured-missions-data');
    let missions = [];
    try { missions = dataEl ? JSON.parse(dataEl.textContent) : []; } catch (_) {}
    createRoot(missionsRoot).render(createElement(FeaturedMissions, { missions }));
  }
} catch (_) {}

// ── Missions List page ───────────────────────────────────
try {
  const listRoot = document.getElementById('missions-list-root');
  if (listRoot) {
    const dataEl = document.getElementById('missions-list-data');
    let missions = [];
    try { missions = dataEl ? JSON.parse(dataEl.textContent) : []; } catch (_) {}
    createRoot(listRoot).render(createElement(FeaturedMissions, { missions }));
  }
} catch (_) {}

// ── Cinematic Footer ─────────────────────────────────────
try {
  const footerRoot = document.getElementById('cinematic-footer-root');
  if (footerRoot) {
    createRoot(footerRoot).render(createElement(CinematicFooter));
  }
} catch (_) {}
