"""SSRF-safe page fetcher: manual redirects (each hop re-validated), size/time limits, HTML to text."""
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from .config import Settings
from .security import UnsafeURLError, no_dns_resolver, validate_public_url

ALLOWED_TYPES = ("text/html", "application/xhtml+xml", "text/plain", "text/markdown")
USER_AGENT = "OAuthSetupGuideBot/1.0 (+research; respects size limits)"

# Phrases that suggest a page is trying to instruct an AI. We never obey them; we flag them.
INJECTION_PATTERNS = [
    r"ignore (all |any )?(previous|prior|above) (instructions|prompts)",
    r"disregard (the |all )?(previous|prior|above|system)",
    r"you are now ",
    r"system prompt",
    r"as an ai (language )?model",
    r"do not (tell|reveal) the user",
    r"new instructions:",
]
_INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.I)


class FetchError(RuntimeError):
    """Fetch failed; message is safe to show."""


@dataclass
class FetchedPage:
    url: str
    final_url: str
    title: str
    text: str
    suspicious: bool


def html_to_text(html: str, max_chars: int) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer", "header", "form", "iframe"]):
        tag.decompose()
    root = soup.find("main") or soup.find("article") or soup.body or soup
    text = root.get_text("\n")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip()
    return title[:300], text[:max_chars]


def looks_like_injection(text: str) -> bool:
    return bool(_INJECTION_RE.search(text))


class Fetcher:
    def __init__(self, settings: Settings, *, validator=validate_public_url, transport: httpx.AsyncBaseTransport | None = None):
        self.s = settings
        if validator is validate_public_url and not settings.ssrf_dns_check:
            validator = lambda u: validate_public_url(u, resolver=no_dns_resolver)  # noqa: E731
        self.validate = validator
        self.transport = transport

    async def fetch(self, url: str) -> FetchedPage:
        current = self.validate(url)
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(self.s.fetch_timeout_s),
            follow_redirects=False,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,text/plain;q=0.9"},
            transport=self.transport,
        ) as client:
            for _ in range(self.s.fetch_max_redirects + 1):
                try:
                    async with client.stream("GET", current) as r:
                        if r.status_code in (301, 302, 303, 307, 308):
                            loc = r.headers.get("location")
                            if not loc:
                                raise FetchError("Redirect without a location.")
                            try:
                                current = self.validate(urljoin(current, loc))
                            except UnsafeURLError as exc:
                                raise FetchError(f"Blocked unsafe redirect: {exc}") from exc
                            continue
                        if r.status_code >= 400:
                            raise FetchError(f"HTTP {r.status_code}")
                        ctype = r.headers.get("content-type", "").split(";")[0].strip().lower()
                        if ctype and ctype not in ALLOWED_TYPES:
                            raise FetchError(f"Unsupported content type '{ctype}'.")
                        buf = bytearray()
                        async for chunk in r.aiter_bytes():
                            buf += chunk
                            if len(buf) > self.s.fetch_max_bytes:
                                break  # truncate, keep what we have
                        enc = r.encoding or "utf-8"
                except httpx.TimeoutException as exc:
                    raise FetchError("Timed out.") from exc
                except httpx.HTTPError as exc:
                    raise FetchError(f"Network error ({type(exc).__name__}).") from exc

                raw = bytes(buf).decode(enc, errors="replace")
                if ctype in ("text/plain", "text/markdown"):
                    title, text = "", raw[: self.s.fetch_max_chars_per_source]
                else:
                    title, text = html_to_text(raw, self.s.fetch_max_chars_per_source)
                if len(text) < 200:
                    raise FetchError("Page had too little readable text (it may need JavaScript).")
                return FetchedPage(url, current, title or current, text, looks_like_injection(text))
        raise FetchError("Too many redirects.")
