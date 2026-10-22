"""Offline evidence-first opportunity scoring.

A high score is NOT a sales forecast or permission to publish.
Input evidence is user/agent supplied and must be independently reviewed.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import json

WEIGHTS = {
    "demand": 25,
    "reader_value": 20,
    "differentiation": 15,
    "evergreen": 15,
    "profit_potential": 10,
    "production_feasibility": 10,
    "maintenance": 5,
}
REQUIRED_KINDS = {"demand", "competition"}
MAX_AGE_DAYS = 180


def _check_scores(scores: dict) -> None:
    missing = sorted(set(WEIGHTS) - set(scores))
    if missing:
        raise ValueError("Missing scores: " + ", ".join(missing))
    for key in WEIGHTS:
        value = scores[key]
        if type(value) not in (int, float) or not 0 <= value <= 10:
            raise ValueError(f"{key}: score must be 0..10")


def _check_evidence(entries: list, today: date) -> tuple[list, int]:
    warnings = []
    domains = set()
    kinds = set()
    for item in entries:
        try:
            address = urlsplit(item["url"])
            observed = date.fromisoformat(item["observed_on"])
            kind = item["kind"]
            if address.scheme != "https" or not address.hostname:
                raise ValueError("HTTPS source required")
            if kind not in ("demand", "competition", "cost", "policy", "other"):
                raise ValueError("unknown evidence kind")
            age = (today - observed).days
            if age < 0 or age > MAX_AGE_DAYS:
                raise ValueError("source not dated in last 180 days")
            if len(item.get("observation", "").strip()) < 12:
                raise ValueError("observation too brief")
            domains.add(address.hostname.removeprefix("www."))
            kinds.add(kind)
        except (KeyError, TypeError, ValueError) as exc:
            warnings.append(f"Invalid evidence: {exc}")
    if len(domains) < 2:
        warnings.append("Fewer than two independent source domains")
    if not REQUIRED_KINDS.issubset(kinds):
        warnings.append("Need recent demand AND competition evidence")
    return warnings, len(domains)


def evaluate_idea(idea: dict, today: date | None = None) -> dict:
    today = today or date.today()
    _check_scores(idea["scores"])
    if not idea.get("id") or not idea.get("title"):
        raise ValueError("Idea needs an id and title")
    rights = idea.get("rights_status", "unverified")
    if rights not in ("clear", "unverified", "blocked"):
        raise ValueError("rights_status must be clear/unverified/blocked")
    risk = idea.get("risk_level", "high")
    if risk not in ("low", "medium", "high"):
        raise ValueError("risk_level must be low/medium/high")
    weighted = sum(idea["scores"][name] * weight / 10
                   for name, weight in WEIGHTS.items())
    warnings, independent_domains = _check_evidence(idea.get("evidence", []), today)
    if rights == "blocked":
        decision = "REJECT"
        warnings.append("Known rights blocker")
    elif warnings or rights != "clear" or risk == "high":
        decision = "HOLD"
        if rights != "clear":
            warnings.append("Rights not independently cleared")
        if risk == "high":
            warnings.append("High risk needs qualified review")
    elif weighted >= 75:
        decision = "CANDIDATE_FOR_HUMAN_REVIEW"
    else:
        decision = "HOLD"
        warnings.append("Score below 75/100 research threshold")
    return {
        "id": idea["id"], "title": idea["title"],
        "score": round(weighted, 2), "status": decision,
        "sources": len(idea.get("evidence", [])),
        "independent_domains": independent_domains,
        "warnings": sorted(set(warnings)),
        "limitations": ("Scores and source observations are agent/user supplied. "
                        "URLs were NOT fetched or independently verified; "
                        "sales and profits are unknown. Human decision required.")
    }


def evaluate_file(path: Path, output: Path | None = None, today: date | None = None) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("ideas"), list):
        raise ValueError("Expected schema_version=1 and ideas array")
    if not data["ideas"]:
        raise ValueError("No ideas to evaluate")
    results = [evaluate_idea(item, today) for item in data["ideas"]]
    results.sort(key=lambda x: (x["status"] == "CANDIDATE_FOR_HUMAN_REVIEW", x["score"]), reverse=True)
    report = {
        "schema_version": 1, "evaluated_on": str(today or date.today()),
        "recommendations": results,
        "note": "No live research performed; no revenue prediction or automatic GO."
    }
    if output:
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite existing report: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report
