# OAuth Setup Guide

Look up an app, get a guide you can follow and share, and know what to do next when registering a provider OAuth app. Six curated guides (GitHub, Google Calendar, Slack, HubSpot, Notion, Salesforce) plus a **live research agent** that builds a guide for any other app.

> **Status.** Curated guides, API, UI, persistence and tests work and were run. The **live generation path (search → fetch → Gemini) needs API keys and open network egress that were not available where this was built**, so it is covered by tests with fake search / LLM / HTTP, *not* by a live run. See [Limitations](#limitations).

## The problem, and the product decision

A developer asks "how hard is it to ship an integration with X?" The answer is really three different things that tools usually blur:

| | What it is | How we show it |
|---|---|---|
| **Developer effort** | Hands-on hours to register and wire the flow | Always labelled *estimate*, with its assumption |
| **Approval wait** | Calendar time someone else controls (review, marketplace, org owner) | Shown separately; a number appears **only if a source states it**, else "Not stated" |
| **Who does what** | What an agent can do vs. what needs a human (accounts, 2FA, legal pages, submitting for review) | Per-step actor badge + two lists |

The second product decision: **every statement carries an evidence status** — `verified` (an official page supports it), `estimate` (our judgement, effort only) or `unverified` (reported but not confirmed) — and anything we could not find goes in an explicit **Unknowns** section. A guide that admits what it doesn't know is more useful than a confident wrong one.

## Quick start

```bash
cp .env.example .env            # fill in keys for live generation (optional for curated guides)

# backend
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:get_app --factory --port 8000

# frontend (second terminal)
cd frontend && npm install && npm run dev      # http://localhost:5173 (proxies /api to :8000)
```

Single-process deployment: `cd frontend && npm run build`, then run the backend; it serves `frontend/dist` and the API from one origin (Docker/Render/Fly: run `uvicorn app.main:get_app --factory --host 0.0.0.0 --port $PORT`; mount a volume at `DATA` path for `DATABASE_PATH`).

Without keys the app works fully for curated guides; `POST /api/guides/generate` for an unknown app returns a clear `503` saying which key is missing.

### Configuration (`.env`, never committed)

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Extraction model (server-side only) |
| `SEARCH_PROVIDER` = `tavily` \| `brave` \| `serper` + that provider's key | Web search for official docs |
| `DATABASE_PATH` | SQLite file |
| `CORS_ORIGINS`, `GENERATE_RATE_LIMIT_PER_MINUTE` | Hardening |
| `SSRF_DNS_CHECK` | Default `true`. Set `false` **only** behind an egress proxy that resolves DNS and filters itself |

## API

`GET /api/health` · `GET /api/guides?q=&difficulty=&source=` · `GET /api/guides/{id}` · `POST /api/guides/generate` (`{"query": "name or URL"}`; `202` + `job_id`, poll `GET /api/jobs/{job_id}` for progress events; `?wait=true` blocks) · `PATCH /api/guides/{id}/progress` (`{"checked": {"step-1": true}}`, per-browser via `X-Client-Id`). Errors are always `{"error": {"code", "message"}}`. Interactive docs at `/api/docs`.

## How the research agent works

```
input ─► validate / SSRF check ─► curated match? ─yes─► return existing guide (no research)
                                        │no
        search (3 queries, rank official-looking hosts first)
                 ▼
        fetch top pages (SSRF-checked on every redirect hop, size/time limits, HTML→text)
                 ▼
        Gemini extracts JSON; pages are wrapped as UNTRUSTED data
                 ▼
        evidence check: quote must appear in the fetched text, else claim ⇒ `unverified`
                 ▼
        Pydantic Guide (rules enforced) ─► SQLite ─► shareable /guides/{id}
```

Trust rules, each with a test:

- **URLs come only from search results or the user's validated URL — never from the model.** The model cites sources by id (`S1`…); unknown ids are dropped.
- A claim is `verified` only if its quote is found in the page text we actually fetched.
- Approval-time numbers survive only with a verified quote; otherwise they become `unknown`.
- Instructions inside pages are ignored and flagged (prompt wording + pattern detector), and surfaced in Unknowns.
- Missing sections (callback rules, testing, publishing) are added to Unknowns automatically.
- Guide confidence (`high/medium/low`) is computed from the share of verified statements and official pages read, not asked of the model.

## Safety

SSRF: only http(s) on ports 80/443, no credentials in URLs, blocks localhost/internal suffixes, private/loopback/link-local/CGNAT/metadata ranges (incl. IPv4-mapped IPv6 and decimal/hex IP forms), DNS answers re-checked, every redirect hop re-validated. Also: input length/charset limits, fetch/search/LLM timeouts, a job timeout, per-IP rate limit, generic 500s, no secrets in responses or frontend. Keys live only in the environment.

## Tests

```bash
cd backend && .venv/bin/python -m pytest -q     # 60 tests: validation, SSRF, evidence checks, generation, persistence, API
cd frontend && npm test && npm run build         # 13 tests + type-check + production build
```

All pass as of 2026-10-29. Not covered by automated tests: real Gemini / search responses.

## What was tested and verified

See **[VERIFICATION.md](VERIFICATION.md)**. In short: 200 claims across the six guides were independently re-checked against official docs; 32 were corrected, 23 could not be supported and are shown as unverified, 2 sources were unreachable; promotions to "verified" required a re-fetch. **No OAuth app was actually created with any provider**, so "verified" means *documentation supports it*, not *we ran it*.

## Where the agent helps vs. where you take over

Agents can: draft the authorize/callback code (state, PKCE), env configuration, refresh handling, request messages to org owners or reviewers, privacy-policy/scope-justification drafts, and smoke tests. Developers must: sign in and create the app (identity, 2FA, org admin), store secrets, submit for review, pass legal/business checks and any security assessment, and respond to reviewers. Each guide lists both explicitly.

## Limitations

- **Live generation not exercised end-to-end here** (no Gemini/search keys; sandbox egress blocked docs sites). Logic is tested with fakes and a mock HTTP transport; expect to tune ranking/prompts on first real runs.
- **JS-rendered docs** (e.g. some Salesforce help pages) return too little text and are skipped; the guide then says so and confidence drops.
- Quote matching tolerates small wording differences (word 4-grams ≥ 85%); it proves the text appears, not that the model understood it.
- DNS is resolved by our check and again by the HTTP client (rebinding window). Production answer: network-level egress filtering.
- In-memory rate limiter and SQLite are single-instance; progress is tied to a browser id, not an account.
- Effort estimates are judgement. Documentation drifts: re-verify before relying on a guide (each shows its date).
- 6 of the target 100 guides are curated; adding more is a new file in `backend/app/seed_data/` plus verification.

## Layout

```
backend/app/   main.py (API) agent.py (pipeline) security.py (SSRF) fetcher.py search.py llm.py db.py models.py
               seed_data/<provider>.py (curated guides)      backend/tests/
frontend/src/  pages/ (Home, GuidePage, GeneratingPage) components/ lib.ts api.ts
verification/  raw/ (200 claim verdicts)  reports/ (per-provider reconciliation)   VERIFICATION.md
```
