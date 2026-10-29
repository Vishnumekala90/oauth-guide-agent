import pytest
from fastapi.testclient import TestClient

from app.agent import ResearchAgent
from app.config import Settings
from app.db import Store
from app.fetcher import Fetcher
from app.main import create_app
from app.search import SearchResult


class FakeSearch:
    name = "fake"

    def __init__(self, results=None):
        self.results = results if results is not None else [
            SearchResult("Acme OAuth docs", "https://developers.acme.com/oauth", "oauth"),
            SearchResult("Acme reddit", "https://reddit.com/r/acme", "chat"),
        ]

    async def search(self, query, num):
        return list(self.results)


class FakeLLM:
    def __init__(self, payload):
        self.payload = payload
        self.prompts = []

    async def generate_json(self, system, prompt):
        self.prompts.append((system, prompt))
        return self.payload


class FakePage:
    def __init__(self, text, suspicious=False):
        self.text, self.suspicious = text, suspicious


PAGE_TEXT = (
    "To register an app open Developer Settings and click Create App. "
    "Redirect URIs must exactly match the registered value. Apps are reviewed within 5 business days. " * 4
)


class FakeFetcher:
    def __init__(self, text=PAGE_TEXT, suspicious=False, fail=False):
        self.text, self.suspicious, self.fail = text, suspicious, fail

    async def fetch(self, url):
        from app.fetcher import FetchedPage, FetchError
        if self.fail:
            raise FetchError("HTTP 404")
        return FetchedPage(url, url, "Acme OAuth", self.text, self.suspicious)


GOOD_PAYLOAD = {
    "provider_name": "Acme",
    "tagline": "Register an app in the dev portal.",
    "difficulty": "easy",
    "difficulty_explanation": "Self-serve.",
    "prerequisites": [{"text": "Developer account", "source_id": "S1", "quote": None}],
    "steps": [
        {"title": "Create app", "detail": "Open Developer Settings and click Create App.", "actor": "developer",
         "source_id": "S1", "quote": "To register an app open Developer Settings and click Create App"},
        {"title": "Fake cite", "detail": "Made up.", "actor": "robot", "source_id": "S9",
         "quote": "this sentence is not on any page at all"},
    ],
    "callback_requirements": [{"text": "Exact match", "source_id": "S1",
                               "quote": "Redirect URIs must exactly match the registered value"}],
    "approval_wait": {"summary": "5 business days", "min_days": 1, "max_days": 5, "source_id": "S1",
                      "quote": "Apps are reviewed within 5 business days"},
    "effort_estimate": {"min_hours": 1, "max_hours": 2, "rationale": "Simple."},
    "unknowns": ["Rate limits"],
}


@pytest.fixture
def settings(tmp_path):
    return Settings(database_path=str(tmp_path / "t.db"), generate_rate_limit_per_minute=100)


@pytest.fixture
def store():
    s = Store(":memory:")
    yield s
    s.close()


def make_client(settings, store, *, llm=None, search=None, fetcher=None):
    agent = ResearchAgent(settings, search, fetcher or FakeFetcher(), llm)
    return TestClient(create_app(settings, store=store, agent=agent))


@pytest.fixture
def client(settings, store):
    return make_client(settings, store, llm=FakeLLM(GOOD_PAYLOAD), search=FakeSearch())


@pytest.fixture
def unconfigured_client(settings, store):
    return make_client(settings, store)
