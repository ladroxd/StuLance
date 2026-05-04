# StuLance — TODO

## High Priority

- [ ] **Student Gig / Service posting system**
  - New `Gig` model: title, description, base_rate (default from `StudentProfile.hourly_rate`), delivery_days, category, skills, is_active
  - `GigExtra` model: label (e.g. "Revision", "Additional feature"), price, delivery_days — linked to a Gig (one-to-many)
  - Student can create/edit/delete their gigs from their profile or a dedicated page (`/gigs/`)
  - Public gig listing page — clients can browse student services (separate from mission listings)
  - Public gig detail page — shows description, base rate, extras table, student profile card
  - Client can contact student directly from gig page (via direct message)
  - Admin can moderate/deactivate gigs

- [ ] **Work delivery / submission system**
  - Student can submit deliverables (file upload or link) from the mission chat/detail page
  - Client can accept or request revision
  - Submission triggers notification to client
  - Submission stored per mission (model: `Submission` with file, link, message, status)

## Performance

- [ ] **Reduce messaging poll delay**
  - Current AJAX polling interval is likely 3s — profile and tune
  - Consider switching to SSE (Server-Sent Events) to eliminate polling overhead entirely

- [ ] **Paginate mission list**
  - Currently loads all open missions at once — add pagination (20 per page)

- [ ] **Add DB indexes**
  - `Mission.status`, `Application.student`, `Notification.user + is_read` — common filter fields with no index

- [ ] **Cache category list**
  - Categories are queried on every mission list load — use `django.core.cache` or template fragment cache

## UX / Frontend

- [ ] **Loading states on messaging**
  - Show a spinner or skeleton while waiting for poll response

- [ ] **Empty state illustrations**
  - Replace plain "No missions" / "No applications" text with a small SVG illustration

- [ ] **Client profile report button**
  - Report button currently only on student profiles and mission detail — add to client profile detail page (`client_profile_detail.html`)

## Features (planned for later CDC revision)

- [ ] **Multi-language completion**
  - Compile updated `.po` → `.mo` for FR and AR after any new translation strings
  - Audit untranslated strings across all new templates (report form, admin stats, earnings banner)

- [ ] **Direct messaging (peer-to-peer)**
  - Already built — wire up properly once added to CDC

## Admin / Moderation

- [ ] **Pending verifications alert**
  - Show a badge/alert in admin navbar when `pending_verifications > 0`

- [ ] **Admin stats: charts**
  - Add a simple Chart.js bar chart for missions by category and a line chart for signups over time
