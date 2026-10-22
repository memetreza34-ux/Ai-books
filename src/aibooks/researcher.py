"""Low-volume, evidence-first live bibliographic research.

Only official Open Library / Google Books catalog endpoints. No web scraping,
sales estimation, AI-token spending, account access, or publication.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
import json
import os
import time

SOURCES = {
    "openlibrary": "https://openlibrary.org/search.json",
    "google_books": "https://www.googleapis.com/books/v1/volumes",
}
MAX_IDEAS = 3
MAX_RESULTS = 10
MAX_RESPONSE_BYTES = 750_000
CACHE_DAYS = 7
RELEVANCE_MODE = "title_contains_required_token"


class ResearchError(ValueError):
    """Invalid spec or malformed third-party catalog response."""


def read_ideas(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    ideas = data.get("ideas") if isinstance(data, dict) else None
    if data.get("schema_version") != 1 or not isinstance(ideas, list):
        raise ResearchError("Expected schema_version 1 with ideas array")
    if not 1 <= len(ideas) <= MAX_IDEAS:
        raise ResearchError(f"Provide between 1 and {MAX_IDEAS} research ideas")
    seen = set()
    for idea in ideas:
        if not isinstance(idea, dict):
            raise ResearchError("Each idea must be a JSON object")
        identifier, query = idea.get("id"), idea.get("query")
        language = idea.get("language", "de")
        must = idea.get("title_must_contain")
        if (not isinstance(identifier, str) or not identifier
            or len(identifier) > 50 or not all(c.isalnum() or c in "-_" for c in identifier)
            or identifier in seen):
            raise ResearchError("IDs must be unique alphanumeric/-/_ strings (max 50)")
        seen.add(identifier)
        if (not isinstance(query, str) or not 2 <= len(query.strip()) <= 90
            or any(ord(ch) < 32 for ch in query)):
            raise ResearchError("Query must contain 2..90 printable characters")
        if language not in {"de", "en", "es", "fr", "it", "nl"}:
            raise ResearchError("Unsupported language code")
        if (not isinstance(must, list) or not 1 <= len(must) <= 3
            or any(not isinstance(t, str) or not 2 <= len(t) <= 30 for t in must)):
            raise ResearchError("title_must_contain must list 1..3 short title terms")
    return ideas


def _normalised_title(title: str) -> str:
    return " ".join(title.casefold().split())


def _matching(title: str, terms: list[str]) -> bool:
    haystack = _normalised_title(title)
    return any(term.casefold() in haystack for term in terms)


def _api_url(source: str, query: str, language: str) -> str:
    if source == "openlibrary":
        params = {"title": query, "lang": language,
                  "limit": str(MAX_RESULTS), "fields": "key,title,author_name,first_publish_year,edition_count,language"}
    elif source == "google_books":
        params = {"q": "intitle:" + query, "langRestrict": language,
                  "maxResults": str(MAX_RESULTS), "printType": "books",
                  "projection": "lite"}
    else:
        raise ResearchError("Unknown data source")
    return SOURCES[source] + "?" + urlencode(params)


def _read_remote_json(url: str, contact: str = "", timeout: float = 10) -> dict:
    # SSRF defence: this function accepts *only* the two hard-coded API URLs.
    parts = urlsplit(url)
    if parts.scheme != "https" or not any(
        url.startswith(root + "?") for root in SOURCES.values()
    ):
        raise ResearchError("Remote URL not in the official API allowlist")
    if any(ord(c) < 32 for c in url):
        raise ResearchError("Invalid URL")
    agent = "Ai-books-research/0.1 (low-volume book research; github.com/memetreza34-ux/Ai-books)"
    if contact:
        agent += " " + contact
    req = Request(url, headers={"User-Agent": agent,
                                "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as response:
        if urlsplit(response.geturl()).hostname != parts.hostname:
            raise ResearchError("Unexpected cross-host API redirect")
        data = response.read(MAX_RESPONSE_BYTES + 1)
    if len(data) > MAX_RESPONSE_BYTES:
        raise ResearchError("API response larger than safety limit")
    try:
        body = json.loads(data)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ResearchError("API returned invalid JSON") from exc
    if not isinstance(body, dict):
        raise ResearchError("Expected JSON object from book API")
    return body


class CatalogClient:
    def __init__(self, cache_dir: Path, fetcher: Callable[[str], dict] | None = None,
                 now: datetime | None = None, contact: str = ""):
        self.cache_dir = cache_dir
        self.fetcher = fetcher or (lambda url: _read_remote_json(url, contact))
        self.now = now or datetime.now(timezone.utc)
        self._next_openlibrary_at = 0.0

    def get(self, source: str, query: str, language: str) -> tuple[dict, dict]:
        url = _api_url(source, query, language)
        cache = self.cache_dir / (sha256(url.encode()).hexdigest() + ".json")
        if cache.is_file():
            try:
                value = json.loads(cache.read_text(encoding="utf-8"))
                stamp = datetime.fromisoformat(value["retrieved_at"])
                if stamp.tzinfo and timedelta(0) <= self.now - stamp <= timedelta(days=CACHE_DAYS):
                    return value["payload"], {"url": url, "retrieved_at": value["retrieved_at"],
                                               "from_cache": True, "sha256": value["sha256"]}
            except (OSError, ValueError, KeyError, TypeError):
                pass
        if source == "openlibrary" and self._next_openlibrary_at > time.monotonic():
            time.sleep(self._next_openlibrary_at - time.monotonic())
        try:
            response = self.fetcher(url)
        finally:
            if source == "openlibrary":
                self._next_openlibrary_at = time.monotonic() + 1.05
        if not isinstance(response, dict):
            raise ResearchError("Non-object API response")
        raw = json.dumps(response, ensure_ascii=False, sort_keys=True).encode("utf-8")
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ResearchError("JSON response larger than safety limit")
        record = {"retrieved_at": self.now.isoformat(),
                  "sha256": sha256(raw).hexdigest(), "payload": response}
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Atomic cache replacement; never store user secrets or scraped pages.
        temp = cache.with_suffix(".temporary")
        temp.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        os.replace(temp, cache)
        return response, {"url": url, "retrieved_at": record["retrieved_at"],
                          "sha256": record["sha256"], "from_cache": False}


def _openlibrary_results(data: dict, terms: list[str]) -> tuple[list, int | None]:
    docs = data.get("docs", [])
    if not isinstance(docs, list):
        raise ResearchError("Open Library malformed docs")
    examples, visited = [], set()
    for d in docs[:MAX_RESULTS]:
        if not isinstance(d, dict) or not isinstance(d.get("title"), str):
            continue
        title = d["title"].strip()
        key = d.get("key", "")
        if not _matching(title, terms) or not isinstance(key, str):
            continue
        # Stable work-level ID only; no arbitrary external record links.
        if key.startswith("/works/"):
            code = key[len("/works/"):]
        else:
            code = key
        if not code.startswith("OL") or not code.endswith("W") or not code[2:-1].isdigit():
            continue
        if code in visited:
            continue
        visited.add(code)
        examples.append({
            "title": title,
            "authors": [str(x) for x in d.get("author_name", [])[:3]] if isinstance(d.get("author_name"), list) else [],
            "published_year": d.get("first_publish_year") if isinstance(d.get("first_publish_year"), int) else None,
            "catalog_url": "https://openlibrary.org/works/" + code,
            "editions_count": d.get("edition_count") if isinstance(d.get("edition_count"), int) else None,
            "kind": "catalog_record_not_a_verified_live_store_offer"
        })
    count = data.get("numFound", data.get("num_found"))
    return examples, count if type(count) is int and count >= 0 else None


def _google_results(data: dict, terms: list[str]) -> tuple[list, int | None]:
    docs = data.get("items", [])
    if not isinstance(docs, list):
        raise ResearchError("Google Books malformed items")
    examples, visited = [], set()
    for d in docs[:MAX_RESULTS]:
        if not isinstance(d, dict):
            continue
        book = d.get("volumeInfo", {})
        if not isinstance(book, dict) or not isinstance(book.get("title"), str):
            continue
        title = book["title"].strip()
        code = d.get("id")
        if (not _matching(title, terms) or not isinstance(code, str)
            or not 1 <= len(code) <= 80 or any(not(c.isalnum() or c in "_-") for c in code)
            or code in visited):
            continue
        visited.add(code)
        authors = book.get("authors")
        examples.append({
            "title": title, "authors": [str(x) for x in authors[:3]] if isinstance(authors, list) else [],
            "published_date": book.get("publishedDate") if isinstance(book.get("publishedDate"), str) else None,
            "page_count": book.get("pageCount") if type(book.get("pageCount")) is int else None,
            "catalog_url": "https://books.google.com/books?id=" + code,
            "kind": "catalog_record_not_a_verified_live_store_offer"
        })
    count = data.get("totalItems")
    return examples, count if type(count) is int and count >= 0 else None


def research_ideas(ideas: list[dict], client: CatalogClient) -> dict:
    output = []
    for idea in ideas:
        sources = []
        for source, parse in (("openlibrary", _openlibrary_results), ("google_books", _google_results)):
            try:
                payload, provenance = client.get(source, idea["query"], idea.get("language", "de"))
                records, reported_count = parse(payload, idea["title_must_contain"])
                sources.append({
                    "source": source, "request": provenance,
                    "status": "ok", "catalog_total_reported": reported_count,
                    "sample_returned": len(records), "examples": records,
                    "disclaimer": "Catalog results are not sales, search volume, or current store availability."
                })
            except (ResearchError, OSError, HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
                sources.append({"source": source, "status": "error",
                                "error": type(exc).__name__ + ": " + str(exc)[:250],
                                "examples": []})
        output.append({
            "id": idea["id"], "query": idea["query"], "language": idea.get("language", "de"),
            "title_must_contain": idea["title_must_contain"],
            "decision": "HOLD", "verified_demand": False, "verified_sales": False,
            "reason": "Catalog coverage alone cannot demonstrate sales demand or profitability.",
            "catalog_sources_ok": sum(s["status"] == "ok" for s in sources),
            "catalog_examples": sum(len(s["examples"]) for s in sources),
            "sources": sources,
            "next_research": ["Verify retailer prices/offer quality manually",
                              "Obtain independently sourced demand signal",
                              "Calculate print costs and royalties for an exact format",
                              "Check original differentiation and content rights"]
        })
    return {
        "schema_version": 1,
        "generated_at": client.now.isoformat(),
        "research_type": "live_catalog_metadata_only",
        "quality": "partial_evidence_not_sales",
        "limit": "No demand, sales, profit or Amazon ranking data obtained.",
        "no_automatic_go": True,
        "ideas": output
    }


def write_report(report: dict, dest: Path) -> Path:
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing research: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def research_file(spec: Path, output: Path, cache_dir: Path, contact: str = "",
                  fetcher: Callable[[str], dict] | None = None,
                  now: datetime | None = None) -> dict:
    ideas = read_ideas(spec)  # validate before any network requests
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing research: {output}")
    client = CatalogClient(cache_dir, fetcher=fetcher, contact=contact, now=now)
    report = research_ideas(ideas, client)
    write_report(report, output)
    return report
