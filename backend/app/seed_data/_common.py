"""Six curated guides, researched against official documentation on 2026-10-28.

Status vocabulary (same as generated guides):
  verified   - a fetched official page supports the statement
  unverified - reported or commonly stated, but NOT confirmed in the pages we read
  estimate   - only used for effort (our own judgement); never for provider policy
Unknown things live in `unknowns`. Nothing here was tested against a live provider account.
"""
from __future__ import annotations

from ..models import ApprovalWait, Blocker, EffortEstimate, Fact, Guide, Source, Step

D = "2026-10-28"

REVIEW_NOTES = [
    "Researched on 2026-10-28 by an AI research agent that read the cited official pages (through a summarizing fetch tool). Selected claims were then re-checked independently; see VERIFICATION.md in the repository for what was confirmed, corrected or left unconfirmed.",
    "'Verified' means a cited official page supports the statement. 'Not verified' means it was reported or is commonly stated but was not confirmed in the pages we read. Nothing here was tested against a live provider account.",
    "Developer-effort figures are our own estimates. Waiting times appear only where the documentation states them.",
]


def src(i: int, title: str, url: str, *, official: bool = True, fetched: bool = True, conf: str = "high", note: str | None = None) -> Source:
    return Source(id=f"S{i}", title=title, url=url, verified_on=D, discovered_via="seed_research",
                  fetched=fetched, official=official, confidence=conf, note=note)


def V(text: str, *sids: str, quote: str | None = None) -> Fact:
    return Fact(text=text, status="verified", source_ids=list(sids), quote=quote)


def U(text: str, *sids: str) -> Fact:
    return Fact(text=text, status="unverified", source_ids=list(sids))


def st(n: int, title: str, detail: str, actor: str, status: str, *sids: str, quote: str | None = None) -> Step:
    return Step(id=f"step-{n}", title=title, detail=detail, actor=actor, status=status, source_ids=list(sids), quote=quote)


def bl(title: str, detail: str, resolution: str | None, status: str, *sids: str) -> Blocker:
    return Blocker(title=title, detail=detail, resolution=resolution, status=status, source_ids=list(sids))
