"""Gemini client (REST). The API key is read server-side only and never returned to clients."""
from __future__ import annotations

import json
import re
from typing import Protocol

import httpx

from .config import Settings


class LLMError(RuntimeError):
    """LLM call failed; message is safe to show."""


class LLM(Protocol):
    async def generate_json(self, system: str, prompt: str) -> dict: ...


def parse_json_loose(text: str) -> dict:
    """Parse a JSON object, tolerating markdown fences the model sometimes adds."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I)
    try:
        data = json.loads(t)
    except json.JSONDecodeError:
        start, end = t.find("{"), t.rfind("}")
        if start == -1 or end <= start:
            raise
        data = json.loads(t[start : end + 1])
    if not isinstance(data, dict):
        raise json.JSONDecodeError("expected a JSON object", t, 0)
    return data


class GeminiClient:
    def __init__(self, settings: Settings):
        self.key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.timeout = settings.gemini_timeout_s

    async def generate_json(self, system: str, prompt: str) -> dict:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        body = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json", "maxOutputTokens": 8192},
        }
        last_err: Exception | None = None
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as c:
                    r = await c.post(url, headers={"x-goog-api-key": self.key, "Content-Type": "application/json"}, json=body)
            except httpx.TimeoutException as exc:
                raise LLMError("The Gemini request timed out. Try again.") from exc
            except httpx.HTTPError as exc:
                raise LLMError("Could not reach the Gemini API.") from exc
            if r.status_code in (400, 401, 403):
                # Never echo the response body: it can contain request details.
                raise LLMError("Gemini rejected the request. Check GEMINI_API_KEY and GEMINI_MODEL.")
            if r.status_code == 429:
                raise LLMError("Gemini rate limit reached. Try again shortly.")
            if r.status_code >= 500:
                last_err = LLMError("Gemini is temporarily unavailable.")
                continue
            if r.status_code >= 400:
                raise LLMError(f"Gemini returned HTTP {r.status_code}.")
            try:
                parts = r.json()["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts)
                return parse_json_loose(text)
            except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
                last_err = LLMError("Gemini returned a response that was not valid JSON.")
                body["contents"][0]["parts"][0]["text"] = prompt + "\n\nReturn ONLY one valid JSON object, no prose."
                continue
        raise last_err or LLMError("Gemini call failed.")


def build_llm(s: Settings) -> LLM | None:
    return GeminiClient(s) if s.gemini_api_key else None
