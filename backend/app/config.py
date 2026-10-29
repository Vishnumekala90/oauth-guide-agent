from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """All secrets come from the environment (or a local, git-ignored .env)."""

    model_config = SettingsConfigDict(env_file=str(ROOT / ".env"), env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_timeout_s: float = 90.0

    # tavily | brave | serper
    search_provider: str = "tavily"
    tavily_api_key: str = ""
    brave_api_key: str = ""
    serper_api_key: str = ""
    search_timeout_s: float = 15.0
    search_results_per_query: int = 8

    # Resolve DNS locally and block private answers. Set false ONLY behind an egress proxy that does its own
    # DNS + filtering (hostname / literal-IP checks still apply).
    ssrf_dns_check: bool = True

    fetch_timeout_s: float = 12.0
    fetch_max_bytes: int = 1_500_000
    fetch_max_chars_per_source: int = 14_000
    fetch_max_redirects: int = 4
    max_sources_to_read: int = 6

    database_path: str = str(ROOT / "data" / "guides.db")
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    generate_rate_limit_per_minute: int = 5
    job_timeout_s: float = 150.0

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
