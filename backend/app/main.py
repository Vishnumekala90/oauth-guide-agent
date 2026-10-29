"""FastAPI application."""
from __future__ import annotations

import asyncio
import logging
import re
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .agent import AgentError, ResearchAgent, new_guide_id
from .config import Settings, get_settings
from .db import Store
from .fetcher import Fetcher
from .llm import build_llm
from .models import (
    GUIDE_ID_RE,
    GenerateRequest,
    GenerateResponse,
    Guide,
    GuideDetail,
    GuideSummary,
    Job,
    ProgressState,
    ProgressUpdate,
)
from .search import build_search_provider
from .security import InputError, UnsafeURLError, no_dns_resolver, parse_query, quick_key, registrable_label, slugify
from .seed_data import SEED_GUIDES

log = logging.getLogger("oauth_guide")
CLIENT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
JOB_ID_RE = re.compile(r"^j-[a-f0-9]{12}$")
SEED_ALIASES = {
    "github": "github", "githubcom": "github",
    "googlecalendar": "google-calendar", "googlecalendarapi": "google-calendar", "gcal": "google-calendar",
    "slack": "slack", "slackcom": "slack",
    "hubspot": "hubspot", "hubspotcom": "hubspot",
    "notion": "notion", "notionso": "notion", "notioncom": "notion",
    "salesforce": "salesforce", "salesforcecom": "salesforce",
}


def error_response(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


class RateLimiter:
    def __init__(self, per_minute: int):
        self.per_minute = per_minute
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= self.per_minute:
            return False
        q.append(now)
        return True


def seed_guides(store: Store) -> None:
    for g in SEED_GUIDES:
        store.save_guide(g)


def match_seed(store: Store, name: str, domain: str | None) -> Guide | None:
    keys = {re.sub(r"[^a-z0-9]", "", name.lower())}
    if domain:
        keys.add(re.sub(r"[^a-z0-9]", "", domain.lower().removeprefix("www.")))
        keys.add(registrable_label(domain))
    for k in keys:
        slug = SEED_ALIASES.get(k)
        if slug:
            return store.find_seed_by_slug(slug)
    return None


def create_app(settings: Settings | None = None, *, store: Store | None = None, agent: ResearchAgent | None = None) -> FastAPI:
    s = settings or get_settings()
    store = store or Store(s.database_path)
    seed_guides(store)
    agent = agent or ResearchAgent(s, build_search_provider(s), Fetcher(s), build_llm(s))
    limiter = RateLimiter(s.generate_rate_limit_per_minute)

    app = FastAPI(title="OAuth Setup Guide API", version="1.0.0", docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.state.store, app.state.agent, app.state.settings = store, agent, s
    app.add_middleware(
        CORSMiddleware, allow_origins=s.cors_origin_list, allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type", "X-Client-Id"], max_age=600,
    )

    # ------------------------------------------------------------------ error shapes
    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):
        first = exc.errors()[0] if exc.errors() else {}
        loc = ".".join(str(x) for x in first.get("loc", []) if x != "body")
        msg = first.get("msg", "Invalid request").removeprefix("Value error, ")
        return error_response(422, "invalid_request", f"{loc + ': ' if loc else ''}{msg}")

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException):
        code = {404: "not_found", 429: "rate_limited"}.get(exc.status_code, "error")
        return error_response(exc.status_code, code, str(exc.detail))

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception):
        log.exception("unhandled error")
        return error_response(500, "internal_error", "Something went wrong on the server. Please try again.")

    # ----------------------------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "guides": store.count_guides(),
            "live_generation": {
                "available": agent.llm is not None and agent.search is not None,
                "llm_configured": agent.llm is not None,
                "search_configured": agent.search is not None,
                "search_provider": s.search_provider,
            },
        }

    @app.get("/api/guides", response_model=list[GuideSummary])
    def list_guides(
        q: str | None = Query(default=None, max_length=100),
        difficulty: str | None = Query(default=None, pattern="^(easy|moderate|hard)$"),
        source: str | None = Query(default=None, pattern="^(seed|agent)$"),
    ):
        items = store.list_guides()
        if q:
            needle = q.strip().lower()
            items = [g for g in items if needle in g.provider_name.lower() or needle in g.tagline.lower() or needle in g.category.lower()]
        if difficulty:
            items = [g for g in items if g.difficulty == difficulty]
        if source:
            items = [g for g in items if g.generated_by == source]
        return items

    @app.get("/api/guides/{guide_id}", response_model=GuideDetail)
    def get_guide(guide_id: str, x_client_id: str | None = Header(default=None)):
        guide = _load(guide_id)
        return GuideDetail(guide=guide, progress=store.get_progress(guide_id, _client(x_client_id)))

    @app.patch("/api/guides/{guide_id}/progress", response_model=ProgressState)
    def patch_progress(guide_id: str, body: ProgressUpdate, x_client_id: str | None = Header(default=None)):
        guide = _load(guide_id)
        valid = set(guide.checklist_ids())
        unknown = sorted(set(body.checked) - valid)
        if unknown:
            raise HTTPException(status_code=422, detail=f"Unknown checklist item(s): {', '.join(unknown[:5])}")
        return store.merge_progress(guide_id, _client(x_client_id), body.checked)

    @app.get("/api/jobs/{job_id}", response_model=Job)
    def get_job(job_id: str):
        if not JOB_ID_RE.match(job_id):
            raise HTTPException(status_code=404, detail="Job not found.")
        job = store.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found.")
        return job

    @app.post("/api/guides/generate", response_model=GenerateResponse, status_code=202)
    async def generate(req: GenerateRequest, request: Request, background: BackgroundTasks, wait: bool = False):
        ip = request.client.host if request.client else "unknown"
        if not limiter.allow(ip):
            raise HTTPException(status_code=429, detail="Too many generation requests. Wait a minute and try again.")
        # Curated guides are matched before any network access (no DNS, no research).
        if not req.force:
            slug = SEED_ALIASES.get(quick_key(req.query) or "")
            seed = store.find_seed_by_slug(slug) if slug else None
            if seed:
                return JSONResponse(
                    status_code=200,
                    content=GenerateResponse(guide_id=seed.id, status="done", existing=True, share_path=f"/guides/{seed.id}").model_dump(),
                )
        try:
            parsed = parse_query(req.query, **({} if s.ssrf_dns_check else {"resolver": no_dns_resolver}))
        except UnsafeURLError as exc:
            return error_response(422, "unsafe_url", str(exc))
        except InputError as exc:
            return error_response(422, "invalid_input", str(exc))

        if not req.force:
            seed = match_seed(store, parsed.name, parsed.domain)
            if seed:
                return JSONResponse(
                    status_code=200,
                    content=GenerateResponse(guide_id=seed.id, status="done", existing=True, share_path=f"/guides/{seed.id}").model_dump(),
                )
        try:
            agent.ensure_configured()
        except AgentError as exc:
            return error_response(503, exc.code, exc.message)

        guide_id, job_id = new_guide_id(), "j-" + uuid.uuid4().hex[:12]
        store.create_job(job_id, guide_id, parsed.raw)
        if wait:
            await _run_job(job_id, guide_id, parsed)
            job = store.get_job(job_id)
            status = 200 if job and job.status == "done" else 502
            return JSONResponse(
                status_code=status,
                content=GenerateResponse(job_id=job_id, guide_id=guide_id, status=job.status if job else "error",
                                         share_path=f"/guides/{guide_id}").model_dump(),
            )
        background.add_task(_run_job, job_id, guide_id, parsed)
        return GenerateResponse(job_id=job_id, guide_id=guide_id, status="queued", share_path=f"/guides/{guide_id}")

    # ---------------------------------------------------------------------- helpers
    async def _run_job(job_id: str, guide_id: str, parsed) -> None:
        store.set_job_status(job_id, "running")

        def progress(stage: str, message: str, level: str = "info") -> None:
            store.add_job_event(job_id, stage, message, level)

        try:
            guide = await asyncio.wait_for(agent.run(parsed, guide_id, progress), timeout=s.job_timeout_s)
            store.save_guide(guide)
            store.add_job_event(job_id, "done", "Guide saved. It has a shareable link.", "info")
            store.set_job_status(job_id, "done")
        except AgentError as exc:
            store.add_job_event(job_id, "error", exc.message, "error")
            store.set_job_status(job_id, "error", exc.message, exc.code)
        except asyncio.TimeoutError:
            msg = "Research took too long and was stopped. Try again, or use the provider's developer docs URL."
            store.add_job_event(job_id, "error", msg, "error")
            store.set_job_status(job_id, "error", msg, "timeout")
        except Exception:  # noqa: BLE001
            log.exception("job %s failed", job_id)
            msg = "Unexpected error while generating the guide."
            store.add_job_event(job_id, "error", msg, "error")
            store.set_job_status(job_id, "error", msg, "internal_error")

    def _load(guide_id: str) -> Guide:
        if not GUIDE_ID_RE.match(guide_id):
            raise HTTPException(status_code=404, detail="Guide not found.")
        g = store.get_guide(guide_id)
        if not g:
            raise HTTPException(status_code=404, detail="Guide not found.")
        return g

    def _client(header: str | None) -> str:
        return header if header and CLIENT_ID_RE.match(header) else "anonymous"

    # ----------------------------------------------- optional: serve built frontend
    dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if dist.is_dir():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str):
            if path.startswith("api/"):
                raise HTTPException(status_code=404, detail="Not found.")
            candidate = (dist / path).resolve()
            if path and candidate.is_file() and dist in candidate.parents:
                return FileResponse(candidate)
            return FileResponse(dist / "index.html")

    return app


def get_app() -> FastAPI:
    """Factory target: `uvicorn app.main:get_app --factory`. Keeps imports side-effect free for tests."""
    return create_app()
