# StuLance — TODO

## High Priority

- [x] **Student Gig / Service posting system**
  - Gig model with extras as JSON field, base_rate, delivery_days, category, skills
  - Student create/edit/delete from `/gigs/my/`
  - Public gig list with search/filter, public gig detail with extras checkboxes
  - Client can contact student directly from gig page via direct message
  - Admin moderation (approve/reject) with status flow

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

## Pre-Traffic UI Polish (do before first real user testing)

- [ ] **Client identity on featured mission cards (home page)**
  - Show company logo/avatar + company name on each glass card so visitors know who posted it
  - Source from `mission.client.company_name` and `mission.client.logo` (or fallback initials avatar)
  - Pass via the JSON data blob already injected by the Django template

- [ ] **General UI refinements before traffic**
  - Review card spacing, font sizes, and contrast on home page for readability
  - Ensure mobile layout of featured missions grid stacks cleanly (1 col on small screens)
  - Check hover states and CTA buttons are consistent across mission cards, gig cards, and navbar
  - Verify footer links are visible on all screen sizes
  - Spot-check dark mode contrast for badges, muted text, and glass card borders

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
