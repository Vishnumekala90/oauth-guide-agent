import time

from app.db import Store
from app.models import Guide
from app.seed_data import SEED_GUIDES

from .conftest import make_client, FakeLLM, FakeSearch, GOOD_PAYLOAD

CID = {"X-Client-Id": "client-abcdef12"}


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["guides"] == 6 and body["live_generation"]["available"] is True


def test_health_reports_unconfigured(unconfigured_client):
    assert unconfigured_client.get("/api/health").json()["live_generation"]["available"] is False


def test_list_and_filter(client):
    items = client.get("/api/guides").json()
    assert {g["id"] for g in items} == {"github", "google-calendar", "slack", "hubspot", "notion", "salesforce"}
    assert [g["id"] for g in client.get("/api/guides?q=slack").json()] == ["slack"]
    hard = client.get("/api/guides?difficulty=hard").json()
    assert hard and all(g["difficulty"] == "hard" for g in hard)
    assert client.get("/api/guides?difficulty=nope").status_code == 422


def test_get_guide_and_404(client):
    d = client.get("/api/guides/github").json()
    assert d["guide"]["provider_name"] == "GitHub" and d["progress"]["checked"] == {}
    assert client.get("/api/guides/does-not-exist").status_code == 404
    assert client.get("/api/guides/..%2f..%2fetc").status_code == 404


def test_progress_roundtrip_is_per_client(client):
    r = client.patch("/api/guides/github/progress", json={"checked": {"step-1": True, "step-2": True}}, headers=CID)
    assert r.status_code == 200 and set(r.json()["checked"]) == {"step-1", "step-2"}
    client.patch("/api/guides/github/progress", json={"checked": {"step-1": False}}, headers=CID)
    assert set(client.get("/api/guides/github", headers=CID).json()["progress"]["checked"]) == {"step-2"}
    assert client.get("/api/guides/github", headers={"X-Client-Id": "other-client-99"}).json()["progress"]["checked"] == {}


def test_progress_rejects_unknown_items(client):
    r = client.patch("/api/guides/github/progress", json={"checked": {"step-99": True}}, headers=CID)
    assert r.status_code == 422
    assert client.patch("/api/guides/github/progress", json={"checked": {}}, headers=CID).status_code == 422
    assert client.patch("/api/guides/nope-nope/progress", json={"checked": {"step-1": True}}).status_code == 404


def test_generate_validation_errors(client):
    assert client.post("/api/guides/generate", json={"query": "a"}).status_code == 422
    assert client.post("/api/guides/generate", json={}).status_code == 422
    r = client.post("/api/guides/generate", json={"query": "http://169.254.169.254/"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "unsafe_url"
    r = client.post("/api/guides/generate", json={"query": "http://localhost:8000"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "unsafe_url"


def test_generate_returns_curated_guide_without_research(client):
    r = client.post("/api/guides/generate", json={"query": "Slack"})
    assert r.status_code == 200 and r.json()["existing"] is True and r.json()["guide_id"] == "slack"


def test_generate_not_configured_is_clear(unconfigured_client):
    r = unconfigured_client.post("/api/guides/generate", json={"query": "Acme"})
    assert r.status_code == 503 and r.json()["error"]["code"] in ("llm_not_configured", "search_not_configured")


def test_generate_end_to_end_persists_shareable_guide(client):
    r = client.post("/api/guides/generate?wait=true", json={"query": "Acme"})
    assert r.status_code == 200, r.text
    gid = r.json()["guide_id"]
    guide = client.get(f"/api/guides/{gid}").json()["guide"]
    assert guide["provider_name"] == "Acme" and guide["generated_by"] == "agent"
    job = client.get(f"/api/jobs/{r.json()['job_id']}").json()
    assert job["status"] == "done" and any(e["stage"] == "search" for e in job["events"])
    assert gid in [g["id"] for g in client.get("/api/guides?source=agent").json()]


def test_generate_background_job_polling(client):
    r = client.post("/api/guides/generate", json={"query": "Acme"})
    assert r.status_code == 202
    job_id = r.json()["job_id"]
    for _ in range(50):
        job = client.get(f"/api/jobs/{job_id}").json()
        if job["status"] in ("done", "error"):
            break
        time.sleep(0.05)
    assert job["status"] == "done"


def test_generate_failure_is_reported_safely(settings, store):
    c = make_client(settings, store, llm=FakeLLM({"provider_name": ""}), search=FakeSearch())
    r = c.post("/api/guides/generate?wait=true", json={"query": "Acme"})
    assert r.status_code == 502
    job = c.get(f"/api/jobs/{r.json()['job_id']}").json()
    assert job["status"] == "error" and job["error_code"] == "llm_invalid"
    assert "Traceback" not in job["error"]


def test_rate_limit(settings, store):
    settings.generate_rate_limit_per_minute = 2
    c = make_client(settings, store, llm=FakeLLM(GOOD_PAYLOAD), search=FakeSearch())
    codes = [c.post("/api/guides/generate", json={"query": "Slack"}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]


def test_persistence_across_store_reopen(tmp_path):
    path = str(tmp_path / "p.db")
    s1 = Store(path)
    g = SEED_GUIDES[0]
    s1.save_guide(g)
    s1.merge_progress(g.id, "client-abcdef12", {"step-1": True})
    s1.close()
    s2 = Store(path)
    assert isinstance(s2.get_guide(g.id), Guide)
    assert s2.get_progress(g.id, "client-abcdef12").checked == {"step-1": True}


def test_seed_guides_are_internally_consistent():
    for g in SEED_GUIDES:
        assert g.sources and g.steps and g.unknowns, g.id
        assert g.effort.short_label.endswith("(estimate)") or "estimate" in g.effort.short_label.lower()
        if g.approval_wait.status in ("unknown", "none_documented"):
            assert g.approval_wait.min_days is None
        assert all(s.official for s in g.sources if s.fetched and s.confidence == "high")


def test_curated_match_needs_no_dns(client, monkeypatch):
    import app.security as sec
    monkeypatch.setattr(sec, "_resolve", lambda h: (_ for _ in ()).throw(AssertionError("DNS used")))
    for q in ("slack.com", "https://www.github.com/docs", "Google Calendar", "notion.so"):
        r = client.post("/api/guides/generate", json={"query": q})
        assert r.status_code == 200 and r.json()["existing"] is True, q
