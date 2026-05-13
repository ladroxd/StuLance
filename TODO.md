# StuLance — TODO

## Next — ASAP

- [x] **Light / Dark theme switch**
  - Add a toggle in the navbar to switch between light and dark mode
  - Persist user preference via `localStorage`
  - Adapt all glass cards, backgrounds, text colors, and navbar for light mode

## High Priority

- [x] **Student Gig / Service posting system**
  - Gig model with extras as JSON field, base_rate, delivery_days, category, skills
  - Student create/edit/delete from `/gigs/my/`
  - Public gig list with search/filter, public gig detail with extras checkboxes
  - Client can contact student directly from gig page via direct message
  - Admin moderation (approve/reject) with status flow

- [x] **Work delivery / submission system**
  - Student can submit deliverables (file upload or link) from the mission chat/detail page
  - Client can accept or request revision
  - Submission triggers notification to client
  - Submission stored per mission (model: `Submission` with file, link, message, status)

## Performance

- [x] **Reduce messaging poll delay**
  - Replaced notification polling entirely with SSE (`/notifications/stream/`) — server pushes within ~1 second, zero wasted requests

- [ ] **Paginate mission list**
  - Currently loads all open missions at once — add pagination (20 per page)

- [ ] **Add DB indexes**
  - `Mission.status`, `Application.student`, `Notification.user + is_read` — common filter fields with no index

- [ ] **Cache category list**
  - Categories are queried on every mission list load — use `django.core.cache` or template fragment cache

## Bug Fixes

- [x] **Footer missing on FR / AR language pages**
  - Root cause: malformed JSON in home template (`|escapejs` producing `\'` for apostrophes) crashed `main.js` before footer could mount
  - Fixed: JSON now serialized in view with `json.dumps()`, crash guards added in `app.js`
  - Footer positioning changed from `fixed` to `absolute` to remove scroll-depth dependency
  - Footer strings now passed via `data-t-*` attributes and translated via `{% trans %}`

- [x] **Chat box white background in direct messages**
  - Direct conversation chatbox used Bootstrap's `#f8f9fa` background and `bg-white border` bubble
  - Fixed: chatbox now uses `var(--navy)`, received bubbles use `.message.received` theme class

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

## UI / Theme

## Production Phase

- [ ] **Switch from `runserver` to Gunicorn with gevent workers**
  - Do NOT use `python manage.py runserver` in production
  - Run the following command instead:
    ```bash
    gunicorn stulance.wsgi:application -c gunicorn.conf.py
    ```
  - Config is already set up in `gunicorn.conf.py` (gevent workers, 1000 connections per worker)
  - Set `DEBUG=False` and configure `ALLOWED_HOSTS` in `.env` before launching

## Admin / Moderation

- [ ] **Pending verifications alert**
  - Show a badge/alert in admin navbar when `pending_verifications > 0`

- [ ] **Admin stats: charts**
  - Add a simple Chart.js bar chart for missions by category and a line chart for signups over time
