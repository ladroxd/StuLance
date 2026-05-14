# StuLance — Project Changelog

How can students access freelance opportunities adapted to their academic schedule, in a secure environment?

---

## Phase 1 — Project Setup & Core Scaffold
**Commit: `ce9fb7e` — Initial commit**

- Initialized Django project (`stulance/`)
- Created 5 Django apps: `accounts`, `missions`, `messaging`, `notifications`, `dashboard`
- Defined all core models:
  - `accounts` — Custom User model with `student` / `client` / `admin` roles, `StudentProfile`, `ClientProfile`, `PortfolioProject`
  - `missions` — `Mission`, `Application`, `Review`, `Category`
  - `messaging` — `Message` (per-mission threaded chat)
  - `notifications` — In-app notification system
- Applied all migrations, seeded 8 mission categories
- Set up `SQLite` as dev database

---

## Phase 2 — README & Documentation
**Commits: `9881cf5` → `5847286` → `747658d`**

- Added comprehensive README (Arabic → English)
- Documented stack, features, team, and setup instructions

---

## Phase 3 — Admin & Jazzmin Theme
**Commit: `a7650dc`**

- Integrated `django-jazzmin` for a modern admin UI
- Configured admin panels for all models
- Renamed "Client" → "Recruiter" in admin UI and model labels (`5f4e0a8`)

---

## Phase 4 — Direct Messaging & Notifications
**Commit: `4d8019b`**

- Added `DirectConversation` and `DirectMessage` models (user-to-user chat)
- Built inbox view with AJAX polling (every 3s)
- Stacked in-app notifications (bell icon, F12 panel)
- Admin dashboard auto-redirect based on user role

---

## Phase 5 — Vite Build Pipeline & UI Overhaul
**Commit: `93a8d9e`**

- Migrated frontend from raw CSS to **Vite** build pipeline
- Introduced the StuLance design system: dark theme, neon accents, glass morphism cards
- Applied consistent styling across all pages (`e88e044`)

---

## Phase 6 — Multi-Language Support (EN / FR / AR)
**Commit: `7695f10`**

- Added Django i18n with `EN`, `FR`, and `AR` translations
- RTL layout support for Arabic using Bootstrap RTL
- Language switcher in navbar
- Sticky footer fix
- Compiled `.po` → `.mo` via Babel (GNU gettext not available on Windows)

---

## Phase 7 — Onboarding & Landing Page
**Commits: `0267327` → `79e04cb`**

- Added role selection onboarding page (student vs recruiter)
- Animated hero background on landing page
- Centered navbar
- FR/AR translations for landing page

---

## Phase 8 — UI Refinements & Bug Fixes
**Commit: `0954e69`**

- Enhanced hero section layout
- Fixed backend bugs in onboarding flow
- Adapted multi-language support to every page (not just landing)
- Removed separate `/register/student` and `/register/client` pages — unified into onboarding flow (`6cf9ec8`)

---

## Phase 9 — Database Migration (SQLite → MySQL)

- Migrated from local SQLite to **Railway cloud MySQL**
- Exported existing data via `dumpdata`, imported via `loaddata`
- App now runs against a persistent cloud database
- Added `logo_neon.png` as browser favicon

---

## Phase 11 — Performance & Notification Dropdown
**Commits: `1a8e511` → `9dd676e` — 2026-05-04**

### Performance Fixes
- Added `CONN_MAX_AGE: 60` to MySQL config — reuses DB connections instead of opening a new TCP connection per request (eliminated 100–300ms per page load)
- Added `dns-prefetch` hints for Bootstrap, Google Fonts CDNs — browser resolves DNS earlier, reducing first-paint delay
- Disabled `use_google_fonts_cdn` in Jazzmin — removed redundant CDN request on admin pages
- Documented: always use `run_local.bat` for dev to avoid Railway DB network latency

### Notification Bell Dropdown
- Converted navbar bell icon from plain link to Bootstrap dropdown
- Dropdown shows last 5 notifications with icon, title, message preview, and unread dot indicator
- Notifications preloaded on page load — instant display on first click (no wait)
- Badge and dropdown content refresh every 30 seconds automatically
- "Mark all read" link and "See all notifications" button at bottom of dropdown
- Fixed Vite closure scoping issue — notification logic moved to inline script in `base.html`
- New JSON endpoint: `GET /notifications/recent/` returns last 5 notifications + unread count

---

## Phase 10 — CDC Gap Analysis & Feature Completion
**Commit: `eec5020` — 2026-05-04**

### CDC Compliance Review
- Performed full audit of the project against the Refined CDC (v1.2)
- Identified and implemented all missing required features (F8 earnings, F11 stats, moderation)

### Student Dashboard — Earnings ("Mes Gains")
- Added total earnings calculation: sum of `budget` across all completed missions where the student was selected
- Displayed as a green gradient earnings banner (in MAD) below the stat cards
- Added **Mission History** section listing all completed missions with date and budget

### Admin Statistics Page (`/dashboard/admin/stats/`)
- New staff-only page with platform-wide metrics:
  - Total students, recruiters, verified students, pending verifications
  - Mission breakdown: open / in progress / completed / total
  - Total applications, average platform rating, total value of completed missions (MAD)
  - Top 5 categories by mission count
- Linked from the navbar dropdown for staff users under "Statistics"

### Report / Flag System
- New `Report` model with: reporter, target (mission or user profile), reason, description, status (pending / reviewed / dismissed)
- Duplicate report prevention per reporter/target pair
- **Report a mission** button on mission detail page (hidden from mission owner)
- **Report a profile** button on student public profile page (hidden from own profile)
- Shared `report_form.html` with radio reason selector (spam / inappropriate / fake / other) and optional description
- Admin panel entry with colored status badges and bulk actions: "Marquer comme traite" / "Rejeter"
- Migration: `missions/0002_report.py`

### Other
- Added `TODO.md` tracking pending features and improvements
- Added logo variants and project assets to `static/images/`
- Added `run_local.bat` and `run_prod.bat` convenience scripts

---

## Phase 12 — Work Delivery / Submission System
**2026-05-06**

- Added `Submission` model (`missions/0003_submission.py`) with fields: mission, student, file upload, link, message, status (`pending` / `accepted` / `revision`)
- Student sees a submit form on in-progress mission detail page (file + link + message, at least one required)
- Client sees all deliverables in a sidebar card with **Accept** and **Request Revision** buttons
- Accepting/requesting revision triggers an in-app notification to the student
- If revision requested, form reappears for the student to resubmit
- Migrated to Railway cloud DB

---

## Phase 13 — Sound System, SSE Notifications & Performance Tooling
**2026-05-07**

### Sound System
- Added `message.mp3` (on send) to both mission chat and direct message pages
- Added `notification.mp3` (on new notification) triggered site-wide via SSE
- Kick click sound restored everywhere except the chat send button
- All sounds lowered to comfortable volume (kick gain `0.18`, mp3s at `30%`)
- Fixed browser autoplay policy issue — message sound plays before `await fetch()` to stay within user gesture; notification sound pre-unlocked on first page click
- Removed kick sound from `src/app.js` React entry (was being compiled into bundle silently)

### SSE — Real-Time Notifications
- Replaced 30-second notification polling with **Server-Sent Events** (`/notifications/stream/`)
- Server pushes badge update within ~1 second of a new notification
- `new: true` flag in SSE payload triggers notification sound only when unread count increases
- Dropdown auto-refreshes on new notification event
- Zero wasted requests when nothing changes

### Performance & Production Readiness
- Installed and configured **Django Debug Toolbar** for dev query profiling
- Installed **Gunicorn + gevent** async workers — handles thousands of concurrent SSE connections without blocking
- Added `gunicorn.conf.py` with gevent worker class, `workers = cpu_count * 2 + 1`, `worker_connections = 1000`
- Added `requirements.txt`
- Documented production run command in `TODO.md` and Notion ("Production Preparation Phase" page)

### Bug Fixes
- Suppressed Django flash messages on chat pages (were showing useless send/receive alerts in the chat UI)
- Wrapped flash messages in `{% block django_messages %}` so individual pages can override

---

## Phase 14 — i18n Footer, Chat Theme & Bug Fixes
**2026-05-07**

### Footer — Full i18n Support
- Footer React component now reads all display strings from `data-t-*` attributes on the root div
- `base.html` passes all footer strings through Django's `{% trans %}` tag — translated server-side before React mounts
- FR and AR `.po` files updated with all footer strings (marquee, buttons, links, copyright)
- `.mo` files recompiled via Babel

### Footer — Visibility Fix Across All Languages
- Root cause of missing footer on FR/AR: home template was manually building JSON with `|escapejs` which produces `\'` for apostrophes — invalid JSON that crashed `main.js` entirely before the footer could mount
- Fixed: JSON now serialized in the view with `json.dumps(ensure_ascii=False)`, guaranteeing valid output
- Added `try/catch` guards in `app.js` around both the missions mount and footer mount so one failure never blocks the other
- Footer positioning changed from `position: fixed` (clip-path scroll-reveal trick) to `position: absolute` — now visible on all pages regardless of scroll depth or content length

### Chat — Dark Theme
- Direct message chatbox background changed from Bootstrap `#f8f9fa` to `var(--navy)`
- Received message bubbles changed from `bg-white border` to `.message.received` (dark glass style matching the rest of the UI)
- Mission chat was already themed — only direct conversation needed fixing

---

## Phase 15 — SSE Stability & Click Sound Fix
**2026-05-07**

### SSE Thread Exhaustion Fix
- SSE stream now has a 55-second lifetime — stream closes and browser auto-reconnects
- Prevents dev server thread pool exhaustion when multiple tabs are open simultaneously (each open tab held a thread indefinitely before; now threads are freed every ~55s)
- Reduced DB poll interval inside the stream from 1s → 2s (halves queries, still fast enough for notifications)

### Click Sound Debounce
- Added 150ms debounce to `_playKick()` using `AudioContext.currentTime`
- Prevents overlapping oscillators caused by rapid/double clicks, which produced a distorted beating artifact
- Oscillators now never fire within 150ms of each other regardless of click speed

---

## Phase 16 — Black & White Theme
**2026-05-13**

### Light / Dark Mode Toggle
- Added a black and white (light/dark) theme switch to the navbar
- User preference persisted via `localStorage` — choice survives page reloads and navigation
- All glass cards, backgrounds, text colors, and navbar adapted for light mode
- CSS variables updated to support both themes across all pages

---

## Phase 17 — Admin Approval Flow, Funds On Hold & UX Fixes
**2026-05-14**

### Admin Mission Approval & Fund Release
- Added **"✅ Approve & mark as completed (release funds)"** bulk action to Mission admin — selects any `in_progress` mission, marks it `completed`, increments student `total_missions`, and sends student a notification
- Added `SubmissionInline` to Mission admin detail page — admin can now see the student's file, link, message and submission status without leaving the mission record
- Registered `Submission` model in admin (`/admin/missions/submission/`) with colored status badges (Pending / Accepted / Revision) and search/filter

### Student Dashboard — Funds On Hold Banner
- New amber banner appears on student dashboard when recruiter has accepted a submission but admin hasn't approved yet
- Shows total amount on hold (sum of pending mission budgets) and a per-mission breakdown with links
- Banner disappears automatically once admin approves and mission moves to `completed`

### Bug Fix — Recruiter Account Not Saved on Registration
- Recruiter onboarding step 4 showed a "You're all set!" page before the account was actually created — closing the tab at that point lost the account entirely
- Fixed: account is now created and saved to DB immediately on step 3 submission, then redirects straight to dashboard

### Report Button on Client Profiles
- Added report button to `client_profile_detail.html` — was only present on student profiles and mission detail pages
- Shown to any authenticated user who isn't the profile owner, same styling and behaviour as student profile report button

### Recruiter "Hire" Button on Gig Pages
- Replaced broken "Contact" link (pointed to POST-only `new_conversation` view, dropped user on inbox) with a proper flow
- New `start_conversation` view at `/messages/start/<user_pk>/` — gets or creates a `DirectConversation` and redirects straight to the chat
- Gig sidebar now shows **"Hire this Student"** (primary button) for recruiters and a ghost "Contact" button for other authenticated users

---

## Current Stack

| Layer | Tech |
|---|---|
| Backend | Django 6.0.4 |
| Database | MySQL (Railway cloud) |
| Frontend | Bootstrap 5, Vite, custom CSS |
| Admin | django-jazzmin |
| i18n | Django i18n — EN / FR / AR |
| Auth | Custom User model (role-based) |
| Realtime | SSE (notifications), AJAX polling (messaging) |
| API | Django REST Framework |
