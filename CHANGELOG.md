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

## Current Stack

| Layer | Tech |
|---|---|
| Backend | Django 6.0.4 |
| Database | MySQL (Railway cloud) |
| Frontend | Bootstrap 5, Vite, custom CSS |
| Admin | django-jazzmin |
| i18n | Django i18n — EN / FR / AR |
| Auth | Custom User model (role-based) |
| Realtime | AJAX polling (messaging & notifications) |
| API | Django REST Framework |
