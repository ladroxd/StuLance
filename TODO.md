# StuLance — TODO

## During Live Prod 

 -  Before Launching Imma need to add these and start monitoring.
 
 --  1 .   Error Tracking      by       'Sentry'.
 --  2 .   Analytics           by       'PostHog'.
 --  3 .   Uptime Monitoring   by       'BetterStack'.
 
 
# Get the Dependencies Audit

- Run NPM audit 
- Lock Versions
- In the requirements.txt file some libs and stuff are missing.


--------------------------------------------------


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

- [x] **Paginate mission list**
  - Currently loads all open missions at once — add pagination (20 per page)
  - Django `Paginator` in `mission_list` view, JSON blob scoped to current page, pagination controls preserve active filters

- [x] **Add DB indexes**
  - `Mission.status`, `Application.student`, `Notification.user + is_read` — common filter fields with no index
  - Also added indexes on `Mission.client/category`, `Application.mission/status`, `Gig.status+is_active/student/category`, `Message.mission+is_read`, `DirectConversation.participant1+2`, `DirectMessage.conversation+is_read`

- [x] **Cache category list**
  - Categories are queried on every mission list load — use `django.core.cache` or template fragment cache
  - Cached for 15 min in `missions/utils.py` (`get_all_categories`), auto-invalidated via signals on Category save/delete
  - Applied in `missions/views.py`, `stulance/views.py`, `gigs/views.py` (4 call sites replaced)

## Bug Fixes

- [x] **Footer missing on FR / AR language pages**
  - Root cause: malformed JSON in home template (`|escapejs` producing `\'` for apostrophes) crashed `main.js` before footer could mount
  - Fixed: JSON now serialized in view with `json.dumps()`, crash guards added in `app.js`
  - Footer positioning changed from `fixed` to `absolute` to remove scroll-depth dependency
  - Footer strings now passed via `data-t-*` attributes and translated via `{% trans %}`

- [x] **Chat box white background in direct messages**
  - Direct conversation chatbox used Bootstrap's `#f8f9fa` background and `bg-white border` bubble
  - Fixed: chatbox now uses `var(--navy)`, received bubbles use `.message.received` theme class

- [x] **Recruiter not being reviewed by admins**
  - ( Needs to be reviewed & the whole company by an admin and approved later )

- [x] **Admin cannot approve completed missions / release funds to student**
  - Added "Approve & mark as completed" bulk action in Mission admin
  - Added Submission inline on Mission admin detail page
  - Registered Submission model in admin with status badges
  - Student dashboard shows "Funds On Hold" amber banner after recruiter accepts submission, disappears once admin approves

- [x] **Recruiter account not saved on DB after onboarding**
  - Step 4 "All Set!" page was shown before account was actually created — user could close tab and account would be lost
  - Fixed: account is now created and saved immediately when step 3 is submitted, then redirected to dashboard
  
- [x] **Forms for filling a mission or gig are not enhanced or perfect.**
  - Redesigned mission create/edit, apply, edit profile, and portfolio forms with themed glass sections, accent inputs, live previews

- [x] **The i18n is still having compatibility issues with some pages**
  - Notifications now translated at display time using key + params system — language switch takes effect instantly on all notifications
  - FR and AR translations added for all notification strings

- [x] **Translation strings missing on mission create and gig create/edit forms**
  - Labels, placeholders, and error messages on `missions/create/` and `gigs/form/` are still hardcoded in French/English
  - Wrapped all strings in `_()` in views and forms; fixed JS extras row in `gigs/form.html` using GIG_I18N object
  - `SubmissionForm` and `ReviewForm` labels/errors translated; flash messages in `missions/views.py` and `gigs/views.py` translated
  - ~70 new entries added to both FR and AR `.po` files — compile with `python manage.py compilemessages` once GNU gettext is installed


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

- [x] **Client profile report button**
  - Report button currently only on student profiles and mission detail — add to client profile detail page (`client_profile_detail.html`)
  
- [x] **Add a button for the recruiters in the gig pages aka Talent**
  - Add a button for recruiters so they can take a gig from a student and work with him.
  - The contact button should redirect to a conversation between the recruiter and the student not to the /messages page where he needs to manually start it.

- [x] **Edit profile for recruiters accessible from profile page**
  - Removed "Edit Profile" from navbar dropdown — button now lives inside the client profile card (visible only to the profile owner)

- [x] **Mission apply — attachment & negotiation**
  - Students can attach supporting documents (portfolio, CV, case study) when applying
  - Students can propose an alternative budget and deadline — shown as chips to the recruiter on the applications page

## Features (planned for later CDC revision)

- [ ] **Multi-language completion**
  - Compile updated `.po` → `.mo` for FR and AR after any new translation strings
  - Audit untranslated strings across all new templates (report form, admin stats, earnings banner)

- [ ] **Direct messaging (peer-to-peer)**
  - Already built — wire up properly once added to CDC

## UI / Theme

- [x] **Improve the Forms**
  - Profile edit, portfolio, mission create/edit, apply forms all redesigned with themed glass sections
  - Skills field on mission form is now a tag input (Enter or comma to add)

- [ ] **In the admin Dashboard implement alerts and notifications on top-right**
- [ ] **Tab badges for unresolved cases**
  - Every tab needs a count of unresolved cases/approvals
  ( e.g. Accounts: Portfolio (1), Recruiter Profiles (4), Student Profiles (8) )

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
