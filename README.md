# MeritMocks

Mock tests for banking, insurance, regulatory and government exams, delivered in the
TCS iON exam-day interface.

## Run locally

```bash
cd src
uv run python manage.py migrate
uv run python manage.py seed_mocks        # catalogue + IBPS PO Prelims free mock (100 Qs)
uv run python manage.py createsuperuser   # optional, for /admin
uv run python manage.py runserver
```

Open http://127.0.0.1:8000. Run the tests with `uv run python manage.py test`.

## Layout

| Path | What it holds |
| --- | --- |
| `src/config/` | Settings (CSP, security headers, production hardening via env vars) |
| `src/core/` | Landing page, brand assets, security-header middleware, rate limiter |
| `src/exams/models.py` | Exam catalogue, mocks, sections, passages, questions, attempts, proctor events |
| `src/exams/engine.py` | Server-authoritative exam engine: timing, section locking, scoring, violations |
| `src/exams/views.py` | Pages and the JSON exam API |
| `src/exams/seed_data/` | Question banks (original content) loaded by `seed_mocks` |
| `src/exams/static/exams/js/` | `exam.js` (exam UI) and `proctor.js` (in-browser exam discipline) |

## Exam integrity

Server side (cannot be bypassed from the browser):

- Correct answers and explanations never reach the browser until the attempt is submitted.
- Questions are served one at a time, only from the section that is currently open, only to
  the session that owns the attempt, and are rate limited.
- The clock lives on the server. Sections advance and the test submits on server time, so
  pausing JavaScript, sleeping the device or editing the page buys no extra time. Answers
  arriving after a section closes are rejected.
- An attempt is bound to one window: opening it elsewhere locks the previous window.
- Focus loss / full-screen exits are counted server-side; at `max_warnings` (default 5) the
  test is auto-submitted. Every event is kept for review in the admin.
- CSP without inline scripts, `X-Frame-Options: DENY`, strict referrer/permissions policies,
  `no-store` on all exam traffic, HttpOnly/SameSite cookies, HSTS and secure cookies in production.

Client side (deterrents): full-screen mode, selection/copy/paste/right-click/print blocked,
devtools and screenshot shortcuts intercepted, content blurred whenever the window loses focus
(this is what snipping tools and screen recorders trigger), and a per-attempt watermark that
restores itself if removed. No website can fully prevent a photo of the screen; the watermark
makes leaks traceable.

## Production settings

Set `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` (comma-separated), then
`manage.py collectstatic` and serve behind HTTPS. Switch `CACHES` to Redis so rate limits are
shared between workers.
