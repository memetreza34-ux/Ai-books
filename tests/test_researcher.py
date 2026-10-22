"""No real HTTP requests in CI; fake provider payloads test the complete workflow."""
from datetime import datetime, timezone, timedelta
import json

import pytest
from aibooks.researcher import (
    CatalogClient, ResearchError, _api_url, _read_remote_json,
    read_ideas, research_file, research_ideas,
)


NOW = datetime(2026, 10, 22, tzinfo=timezone.utc)
IDEAS = {"schema_version": 1, "ideas": [{
    "id": "sudoku-de", "query": "Sudoku Großdruck", "language": "de",
    "title_must_contain": ["sudoku"]
}]}

OL = {"numFound": 9000, "docs": [
    {"key": "/works/OL12345W", "title": "Sudoku Großdruck", "author_name": ["Beispiel"],
     "first_publish_year": 2010, "edition_count": 2},
    {"key": "/works/OL12346W", "title": "Fremdes Kochbuch"},
]}
APPLE = {"resultCount": 123, "results": [
    {"trackName": "Das Sudoku Buch", "trackViewUrl": "https://books.apple.com/de/book/id12345",
     "artistName": "Beispiel", "trackPrice": 4.99, "currency": "EUR"},
    {"trackName": "Pizza", "trackViewUrl": "https://books.apple.com/de/book/id98765"}
]}


def fetcher(url):
    if url.startswith("https://openlibrary.org/search.json?"):
        return OL
    if url.startswith("https://itunes.apple.com/search?"):
        return APPLE
    raise AssertionError("Unexpected source URL " + url)


def test_real_catalog_pipeline_does_not_claim_demand(tmp_path):
    inp = tmp_path / "ideas.json"
    out = tmp_path / "report.json"
    inp.write_text(json.dumps(IDEAS), encoding="utf-8")
    report = research_file(inp, out, tmp_path / "cache", fetcher=fetcher, now=NOW)
    idea = report["ideas"][0]
    assert out.is_file()
    assert report["no_automatic_go"] and idea["decision"] == "HOLD"
    assert not idea["verified_sales"] and not idea["verified_demand"]
    assert idea["catalog_sources_ok"] == 2
    assert idea["catalog_examples"] == 2
    assert idea["sources"][0]["catalog_total_reported"] == 9000
    assert idea["sources"][0]["sample_returned"] == 1
    assert idea["sources"][0]["examples"][0]["catalog_url"].endswith("OL12345W")
    assert idea["sources"][1]["examples"][0]["catalog_url"].endswith("id12345")
    assert idea["sources"][0]["request"]["sha256"]
    with pytest.raises(FileExistsError):
        research_file(inp, out, tmp_path / "cache", fetcher=fetcher, now=NOW)


def test_cache_reuses_results_without_hidden_calls(tmp_path):
    count = []
    def fake(url):
        count.append(url)
        return fetcher(url)
    client = CatalogClient(tmp_path / "cache", fetcher=fake, now=NOW)
    first = research_ideas(IDEAS["ideas"], client)
    second = research_ideas(IDEAS["ideas"], client)
    assert len(count) == 2
    assert first["ideas"][0]["sources"][0]["request"]["from_cache"] is False
    assert second["ideas"][0]["sources"][0]["request"]["from_cache"] is True


def test_old_cache_refetched(tmp_path):
    old = CatalogClient(tmp_path / "cache", fetcher=fetcher, now=NOW - timedelta(days=9))
    old.get("apple_books", "Sudoku Großdruck", "de")
    calls = []
    new = CatalogClient(tmp_path / "cache", fetcher=lambda u: (calls.append(u) or APPLE), now=NOW)
    _, provenance = new.get("apple_books", "Sudoku Großdruck", "de")
    assert len(calls) == 1 and not provenance["from_cache"]


def test_provider_error_isolated_and_hold(tmp_path):
    def partial(url):
        if "openlibrary" in url:
            raise TimeoutError("timeout")
        return APPLE
    client = CatalogClient(tmp_path / "cache", fetcher=partial, now=NOW)
    result = research_ideas(IDEAS["ideas"], client)["ideas"][0]
    assert result["catalog_sources_ok"] == 1
    assert result["sources"][0]["status"] == "error"
    assert result["decision"] == "HOLD"


@pytest.mark.parametrize("ideas", [
    [], [IDEAS["ideas"][0]] * 4,
    [{"id":"a", "query":"x", "title_must_contain":["x"]}],
    [{"id":"../../bad", "query":"Sudoku", "title_must_contain":["sudoku"]}],
    [{"id":"a", "query":"Sudoku", "language":"zz","title_must_contain":["sudoku"]}],
])
def test_input_rejects_invalid_spec(tmp_path, ideas):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_version":1, "ideas":ideas}))
    with pytest.raises(ResearchError):
        read_ideas(path)


def test_remote_allowlist_enforced():
    with pytest.raises(ResearchError):
        _read_remote_json("https://example.com/secrets")


def test_stale_and_malformed_payload_hold(tmp_path):
    client = CatalogClient(tmp_path / "cache",
                           fetcher=lambda u: {"docs":"not-a-list"} if "openlibrary" in u else {"items":[]},
                           now=NOW)
    result = research_ideas(IDEAS["ideas"], client)["ideas"][0]
    assert result["decision"] == "HOLD"
    assert result["catalog_sources_ok"] == 1


def test_official_api_query_params():
    ol = _api_url("openlibrary", "Sudoku Großdruck", "de")
    google = _api_url("apple_books", "Sudoku Großdruck", "de")
    assert "fields=" in ol and "limit=10" in ol
    assert "country=DE" in google and "limit=10" in google
    assert "https://" in ol


def test_provider_rate_limit_stops_subsequent_calls(tmp_path):
    from urllib.error import HTTPError
    calls = []
    def fake(url):
        calls.append(url)
        if "itunes.apple.com" in url:
            raise HTTPError(url, 429, "Too Many Requests", hdrs=None, fp=None)
        return OL
    two = [dict(IDEAS["ideas"][0], id="first"),
           dict(IDEAS["ideas"][0], id="second")]
    client = CatalogClient(tmp_path / "cache", fetcher=fake, now=NOW)
    report = research_ideas(two, client)
    assert [r["decision"] for r in report["ideas"]] == ["HOLD", "HOLD"]
    assert len([x for x in calls if "itunes.apple.com" in x]) == 1
    assert report["ideas"][0]["sources"][1]["status"] == "error"
    assert report["ideas"][1]["sources"][1]["status"] == "skipped_rate_limit"


def test_tampered_cache_is_not_trusted(tmp_path):
    client = CatalogClient(tmp_path / "cache", fetcher=fetcher, now=NOW)
    client.get("apple_books", "Sudoku Großdruck", "de")
    cache = next((tmp_path / "cache").glob("*.json"))
    record = json.loads(cache.read_text(encoding="utf-8"))
    record["payload"]["resultCount"] = 999999
    cache.write_text(json.dumps(record), encoding="utf-8")
    refreshed = []
    again = CatalogClient(tmp_path / "cache",
                          fetcher=lambda url: (refreshed.append(url) or APPLE), now=NOW)
    body, meta = again.get("apple_books", "Sudoku Großdruck", "de")
    assert refreshed and body["resultCount"] == APPLE["resultCount"]
    assert not meta["from_cache"]
