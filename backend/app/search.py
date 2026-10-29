"""Configurable web search providers. Results are the only source of URLs the agent may cite."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import httpx

from .config import Settings


class SearchError(RuntimeError):
    """Search failed; message is safe to show to users."""


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class SearchProvider(Protocol):
    name: str

    async def search(self, query: str, num: int) -> list[SearchResult]: ...


class TavilySearch:
    name = "tavily"

    def __init__(self, api_key: str, timeout: float):
        self.api_key, self.timeout = api_key, timeout

    async def search(self, query: str, num: int) -> list[SearchResult]:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.post(
                "https://api.tavily.com/search",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"query": query, "max_results": num, "search_depth": "basic"},
            )
        _raise_for_status(r, "Tavily")
        return [
            SearchResult(x.get("title") or x["url"], x["url"], (x.get("content") or "")[:400])
            for x in r.json().get("results", [])
            if x.get("url")
        ]


class BraveSearch:
    name = "brave"

    def __init__(self, api_key: str, timeout: float):
        self.api_key, self.timeout = api_key, timeout

    async def search(self, query: str, num: int) -> list[SearchResult]:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": self.api_key, "Accept": "application/json"},
                params={"q": query, "count": num},
            )
        _raise_for_status(r, "Brave Search")
        items = r.json().get("web", {}).get("results", [])
        return [SearchResult(x.get("title") or x["url"], x["url"], (x.get("description") or "")[:400]) for x in items if x.get("url")]


class SerperSearch:
    name = "serper"

    def __init__(self, api_key: str, timeout: float):
        self.api_key, self.timeout = api_key, timeout

    async def search(self, query: str, num: int) -> list[SearchResult]:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": self.api_key},
                json={"q": query, "num": num},
            )
        _raise_for_status(r, "Serper")
        return [
            SearchResult(x.get("title") or x["link"], x["link"], (x.get("snippet") or "")[:400])
            for x in r.json().get("organic", [])
            if x.get("link")
        ]


def _raise_for_status(r: httpx.Response, label: str) -> None:
    if r.status_code in (401, 403):
        raise SearchError(f"{label} rejected the API key. Check the search key in your environment.")
    if r.status_code == 429:
        raise SearchError(f"{label} rate limit reached. Try again shortly.")
    if r.status_code >= 400:
        raise SearchError(f"{label} returned HTTP {r.status_code}.")


def build_search_provider(s: Settings) -> SearchProvider | None:
    """Return a provider, or None when no key is configured (the API reports this clearly)."""
    p = s.search_provider.lower()
    if p == "tavily" and s.tavily_api_key:
        return TavilySearch(s.tavily_api_key, s.search_timeout_s)
    if p == "brave" and s.brave_api_key:
        return BraveSearch(s.brave_api_key, s.search_timeout_s)
    if p == "serper" and s.serper_api_key:
        return SerperSearch(s.serper_api_key, s.search_timeout_s)
    return None
