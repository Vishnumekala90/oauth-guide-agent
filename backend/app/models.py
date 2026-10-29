"""Pydantic models for guides, evidence, jobs and API payloads.

Design rule: every statement in a guide is either
  * verified   - a source we actually fetched supports it (quote checked for generated guides),
  * estimate   - a labelled judgement, never presented as provider policy, or
  * unverified - we saw it but could not confirm it against fetched text.
Anything we could not find goes in `unknowns`.
"""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

ClaimStatus = Literal["verified", "estimate", "unverified"]
Difficulty = Literal["easy", "moderate", "hard"]
Actor = Literal["agent", "developer", "both"]
Confidence = Literal["high", "medium", "low"]
WaitStatus = Literal["documented", "estimate", "unknown", "none_documented"]

GUIDE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")


class Source(BaseModel):
    id: str = Field(pattern=r"^S\d{1,2}$")
    title: str = Field(min_length=1, max_length=300)
    url: str = Field(min_length=8, max_length=2000)
    verified_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    discovered_via: Literal["search", "user_input", "seed_research"]
    fetched: bool
    official: bool = Field(description="Heuristic: hostname looks like the provider's own docs/developer site")
    confidence: Confidence
    note: str | None = Field(default=None, max_length=500)

    @field_validator("url")
    @classmethod
    def _http_only(cls, v: str) -> str:
        if not v.lower().startswith(("http://", "https://")):
            raise ValueError("source url must be http(s)")
        return v


class Fact(BaseModel):
    text: str = Field(min_length=1, max_length=1200)
    status: ClaimStatus
    source_ids: list[str] = Field(default_factory=list)
    quote: str | None = Field(default=None, max_length=600)

    @model_validator(mode="after")
    def _verified_needs_source(self) -> "Fact":
        if self.status == "verified" and not self.source_ids:
            raise ValueError("a verified fact must cite at least one source")
        return self


class Step(BaseModel):
    id: str = Field(pattern=r"^step-\d{1,2}$")
    title: str = Field(min_length=1, max_length=200)
    detail: str = Field(min_length=1, max_length=1500)
    actor: Actor
    status: ClaimStatus
    source_ids: list[str] = Field(default_factory=list)
    quote: str | None = Field(default=None, max_length=600)


class Blocker(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    detail: str = Field(min_length=1, max_length=1200)
    resolution: str | None = Field(default=None, max_length=1200)
    status: ClaimStatus
    source_ids: list[str] = Field(default_factory=list)
    quote: str | None = Field(default=None, max_length=600)


class ApprovalWait(BaseModel):
    """Waiting time that is NOT developer effort. Numbers only when a source states them."""

    short_label: str = Field(min_length=1, max_length=80)
    summary: str = Field(min_length=1, max_length=1200)
    status: WaitStatus
    min_days: int | None = Field(default=None, ge=0, le=730)
    max_days: int | None = Field(default=None, ge=0, le=730)
    source_ids: list[str] = Field(default_factory=list)
    quote: str | None = Field(default=None, max_length=600)

    @model_validator(mode="after")
    def _numbers_need_documentation(self) -> "ApprovalWait":
        if self.status in ("unknown", "none_documented") and (self.min_days or self.max_days):
            raise ValueError("unknown / none_documented waits must not carry numbers")
        if self.status == "documented" and not self.source_ids:
            raise ValueError("a documented wait must cite a source")
        if self.min_days is not None and self.max_days is not None and self.min_days > self.max_days:
            raise ValueError("min_days > max_days")
        return self


class EffortEstimate(BaseModel):
    """Developer hands-on time. Always an estimate; the rationale says what it assumes."""

    short_label: str = Field(min_length=1, max_length=80)
    min_hours: float = Field(ge=0, le=500)
    max_hours: float = Field(ge=0, le=500)
    rationale: str = Field(min_length=1, max_length=800)

    @model_validator(mode="after")
    def _ordered(self) -> "EffortEstimate":
        if self.min_hours > self.max_hours:
            raise ValueError("min_hours > max_hours")
        return self


class Guide(BaseModel):
    id: str
    slug: str
    provider_name: str = Field(min_length=1, max_length=120)
    tagline: str = Field(min_length=1, max_length=300)
    category: str = Field(min_length=1, max_length=60)
    website: str | None = None
    generated_by: Literal["seed", "agent"]
    verified_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    overall_confidence: Confidence
    difficulty: Difficulty
    difficulty_explanation: str = Field(min_length=1, max_length=1200)
    effort: EffortEstimate
    approval_wait: ApprovalWait
    prerequisites: list[Fact] = Field(default_factory=list)
    steps: list[Step] = Field(default_factory=list)
    callback_requirements: list[Fact] = Field(default_factory=list)
    scopes: list[Fact] = Field(default_factory=list)
    testing: list[Fact] = Field(default_factory=list)
    publishing: list[Fact] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    agent_can_do: list[str] = Field(default_factory=list)
    developer_must_do: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    review_notes: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _id_shape(cls, v: str) -> str:
        if not GUIDE_ID_RE.match(v):
            raise ValueError("invalid guide id")
        return v

    @model_validator(mode="after")
    def _references_resolve(self) -> "Guide":
        known = {s.id for s in self.sources}
        if len(known) != len(self.sources):
            raise ValueError("duplicate source ids")
        used: list[str] = []
        for group in (self.prerequisites, self.callback_requirements, self.scopes, self.testing, self.publishing):
            for f in group:
                used += f.source_ids
        for s in self.steps:
            used += s.source_ids
        for b in self.blockers:
            used += b.source_ids
        used += self.approval_wait.source_ids
        missing = sorted(set(used) - known)
        if missing:
            raise ValueError(f"citations reference unknown sources: {missing}")
        return self

    def checklist_ids(self) -> list[str]:
        return [s.id for s in self.steps]


class GuideSummary(BaseModel):
    id: str
    slug: str
    provider_name: str
    tagline: str
    category: str
    generated_by: Literal["seed", "agent"]
    difficulty: Difficulty
    effort_label: str
    approval_label: str
    approval_status: WaitStatus
    overall_confidence: Confidence
    verified_on: str


def summarize(g: Guide) -> GuideSummary:
    return GuideSummary(
        id=g.id,
        slug=g.slug,
        provider_name=g.provider_name,
        tagline=g.tagline,
        category=g.category,
        generated_by=g.generated_by,
        difficulty=g.difficulty,
        effort_label=g.effort.short_label,
        approval_label=g.approval_wait.short_label,
        approval_status=g.approval_wait.status,
        overall_confidence=g.overall_confidence,
        verified_on=g.verified_on,
    )


# ---------------------------------------------------------------- API payloads

class GenerateRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200, description="App name or website URL")
    force: bool = Field(default=False, description="Regenerate even if a curated guide exists")

    @field_validator("query")
    @classmethod
    def _clean(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("query too short")
        if any(ord(c) < 32 for c in v):
            raise ValueError("control characters are not allowed")
        return v


class ProgressUpdate(BaseModel):
    checked: dict[str, bool] = Field(min_length=1, max_length=60)


class ProgressState(BaseModel):
    checked: dict[str, bool] = Field(default_factory=dict)
    updated_at: str | None = None


class GuideDetail(BaseModel):
    guide: Guide
    progress: ProgressState


class JobEvent(BaseModel):
    ts: str
    stage: str
    message: str
    level: Literal["info", "warn", "error"] = "info"


class Job(BaseModel):
    id: str
    guide_id: str
    query: str
    status: Literal["queued", "running", "done", "error"]
    events: list[JobEvent] = Field(default_factory=list)
    error: str | None = None
    error_code: str | None = None
    created_at: str
    updated_at: str


class GenerateResponse(BaseModel):
    job_id: str | None = None
    guide_id: str
    status: Literal["queued", "running", "done", "error"]
    existing: bool = False
    share_path: str
