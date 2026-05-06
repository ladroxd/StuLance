import { createElement as h, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const CATEGORY_IMAGES = {
  web:     'photo-1627398242454-45a1465c2479', // code on screen
  front:   'photo-1627398242454-45a1465c2479',
  back:    'photo-1558494949-ef010cbdcc31', // server rack
  design:  'photo-1561070791-2526d30994b5', // design tools
  ui:      'photo-1561070791-2526d30994b5',
  ux:      'photo-1561070791-2526d30994b5',
  mobile:  'photo-1512941937669-90a1b58e7e9c', // mobile phone
  android: 'photo-1512941937669-90a1b58e7e9c',
  ios:     'photo-1512941937669-90a1b58e7e9c',
  data:    'photo-1551288049-bebda4e38f71', // data charts
  ai:      'photo-1677442135703-1787eea5ce01', // AI abstract
  ml:      'photo-1677442135703-1787eea5ce01',
  video:   'photo-1574717024653-61fd2cf4d44d', // camera/film
  motion:  'photo-1574717024653-61fd2cf4d44d',
  write:   'photo-1455390582262-044cdead277a', // writing
  content: 'photo-1455390582262-044cdead277a',
  copy:    'photo-1455390582262-044cdead277a',
  market:  'photo-1533750349088-cd871a92f312', // marketing
  social:  'photo-1611162617213-7d7a39e9b1d7', // social media
  seo:     'photo-1533750349088-cd871a92f312',
};

const CATEGORY_ICONS = {
  web: 'bi-code-slash', front: 'bi-code-slash', back: 'bi-code-slash',
  design: 'bi-palette', ui: 'bi-palette', ux: 'bi-palette',
  mobile: 'bi-phone', android: 'bi-phone', ios: 'bi-phone',
  data: 'bi-bar-chart-line', ai: 'bi-bar-chart-line', ml: 'bi-bar-chart-line',
  video: 'bi-camera-video', motion: 'bi-camera-video',
  write: 'bi-pencil-square', content: 'bi-pencil-square', copy: 'bi-pencil-square',
  market: 'bi-megaphone', social: 'bi-megaphone', seo: 'bi-megaphone',
};

function getCategoryImage(categoryName = '') {
  const lower = categoryName.toLowerCase();
  for (const [key, id] of Object.entries(CATEGORY_IMAGES)) {
    if (lower.includes(key)) return `https://images.unsplash.com/${id}?w=480&q=75&fit=crop&auto=format`;
  }
  return `https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=480&q=75&fit=crop&auto=format`; // default office
}

function getCategoryIcon(categoryName = '') {
  const lower = categoryName.toLowerCase();
  for (const [key, icon] of Object.entries(CATEGORY_ICONS)) {
    if (lower.includes(key)) return icon;
  }
  return 'bi-briefcase';
}

function MissionCard({ mission, index }) {
  const icon = getCategoryIcon(mission.category);
  const image = getCategoryImage(mission.category);

  return h(motion.div, {
    key: mission.pk,
    initial: { opacity: 0, y: 24 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.4, delay: index * 0.08 },
    style: { width: '100%' },
  },
    h('a', { href: `/missions/${mission.pk}/`, style: { textDecoration: 'none', color: 'inherit' } },
      h(motion.div, {
        className: 'mission-glass-card',
        whileHover: { y: -4, boxShadow: '0 20px 60px rgba(124,58,237,0.25)' },
        transition: { type: 'spring', stiffness: 300, damping: 24 },
        style: {
          borderRadius: '1rem',
          overflow: 'hidden',
          background: 'rgba(255,255,255,0.04)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          border: '1px solid rgba(124,58,237,0.2)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.25)',
          transition: 'border-color 0.3s',
          cursor: 'pointer',
        },
      },
        /* Image / thumbnail */
        h('div', {
          style: {
            position: 'relative',
            height: '140px',
            backgroundImage: `url(${image})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
          },
        },
          h('i', {
            className: `bi ${icon}`,
            style: { fontSize: '2.2rem', color: '#fff', opacity: 0.9, position: 'relative', zIndex: 1, filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.6))' },
          }),
          /* gradient overlay */
          h('div', {
            style: {
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(to top, rgba(10,10,10,0.5) 0%, transparent 60%)',
            },
          }),
          /* tags */
          h('div', { style: { position: 'absolute', bottom: '10px', left: '12px', display: 'flex', gap: '6px' } },
            h('span', {
              style: {
                background: 'rgba(124,58,237,0.55)',
                backdropFilter: 'blur(8px)',
                color: '#fff',
                fontSize: '11px',
                fontWeight: 600,
                padding: '2px 10px',
                borderRadius: '999px',
                border: '1px solid rgba(124,58,237,0.4)',
              },
            }, mission.category),
          ),
          /* hover overlay */
          h(motion.div, {
            className: 'mission-card-hover-overlay',
            initial: { opacity: 0 },
            whileHover: { opacity: 1 },
            style: {
              position: 'absolute',
              inset: 0,
              background: 'rgba(10,10,10,0.35)',
              backdropFilter: 'blur(2px)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'opacity 0.3s',
              zIndex: 2,
            },
          },
            h(motion.span, {
              whileHover: { scale: 1.05 },
              whileTap: { scale: 0.95 },
              style: {
                background: 'var(--accent, #7c3aed)',
                color: '#fff',
                fontSize: '13px',
                fontWeight: 600,
                padding: '8px 22px',
                borderRadius: '999px',
                boxShadow: '0 4px 20px rgba(124,58,237,0.4)',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              },
            },
              h('i', { className: 'bi bi-arrow-right-circle' }),
              'View Mission',
            ),
          ),
        ),

        /* Content */
        h('div', { style: { padding: '18px 20px', display: 'flex', flexDirection: 'column', gap: '12px' } },
          h('div', {},
            h('h3', {
              style: {
                fontSize: '16px',
                fontWeight: 700,
                color: '#f0f0f0',
                marginBottom: '6px',
                lineHeight: 1.35,
              },
            }, mission.title),
            h('p', {
              style: {
                fontSize: '13px',
                color: '#888',
                lineHeight: 1.55,
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
              },
            }, mission.description),
          ),

          /* Skills */
          mission.skills && mission.skills.length > 0 && h('div', { style: { display: 'flex', flexWrap: 'wrap', gap: '6px' } },
            mission.skills.slice(0, 3).map((skill, i) =>
              h('span', {
                key: i,
                style: {
                  background: 'rgba(124,58,237,0.12)',
                  color: '#a78bfa',
                  fontSize: '11px',
                  fontWeight: 500,
                  padding: '2px 10px',
                  borderRadius: '999px',
                  border: '1px solid rgba(124,58,237,0.2)',
                },
              }, skill)
            ),
          ),

          /* Client identity */
          mission.company_name && h('div', {
            style: { display: 'flex', alignItems: 'center', gap: '8px' },
          },
            h('div', {
              style: {
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #7c3aed, #a78bfa)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '10px',
                fontWeight: 700,
                color: '#fff',
                flexShrink: 0,
              },
            }, mission.company_name.charAt(0).toUpperCase()),
            h('span', {
              style: { fontSize: '12px', color: '#aaa', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' },
            }, mission.company_name),
          ),

          /* Footer */
          h('div', {
            style: {
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTop: '1px solid rgba(124,58,237,0.15)',
              paddingTop: '12px',
              marginTop: '2px',
            },
          },
            h('div', {},
              h('div', {
                style: { fontFamily: "'DM Mono', monospace", fontWeight: 700, color: 'var(--accent, #7c3aed)', fontSize: '15px' },
              }, `${mission.budget} MAD`),
              h('div', { style: { fontSize: '11px', color: '#666', marginTop: '2px' } },
                h('i', { className: 'bi bi-clock me-1' }),
                `${mission.deadline_days} days`,
              ),
            ),
            h('span', {
              style: { fontSize: '11px', color: '#666' },
            },
              h('i', { className: 'bi bi-people me-1' }),
              `${mission.applications_count} applicant${mission.applications_count !== 1 ? 's' : ''}`,
            ),
          ),
        ),
      ),
    ),
  );
}

export function FeaturedMissions({ missions }) {
  return h('div', {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
      gap: '24px',
      width: '100%',
    },
  },
    missions.map((m, i) => h(MissionCard, { key: m.pk, mission: m, index: i }))
  );
}
