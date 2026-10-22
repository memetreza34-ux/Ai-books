import json
from datetime import date
from pathlib import Path
import pytest

from aibooks.opportunities import evaluate_idea, evaluate_file


def example(today):
    return {
        "id": "test-only", "title": "Sample (hypothetical)",
        "rights_status": "clear", "risk_level": "low",
        "scores": dict(demand=8, reader_value=9, differentiation=8,
                       evergreen=9, profit_potential=7,
                       production_feasibility=9, maintenance=9),
        "evidence": [
            {"url": "https://amazon.de/example", "observed_on": str(today),
             "kind": "competition", "observation": "Hypothetical competitor listing"},
            {"url": "https://trends.google.com/example", "observed_on": str(today),
             "kind": "demand", "observation": "Hypothetical demand signal"},
        ]
    }


def test_complete_evidence_only_reaches_human_review():
    d = date(2026, 10, 22)
    answer = evaluate_idea(example(d), d)
    assert answer["status"] == "CANDIDATE_FOR_HUMAN_REVIEW"
    assert answer["score"] >= 75
    assert "URLs were NOT fetched" in answer["limitations"]


def test_missing_market_data_stays_on_hold():
    d = date(2026, 10, 22)
    idea = example(d)
    idea["evidence"] = []
    answer = evaluate_idea(idea, d)
    assert answer["status"] == "HOLD"


def test_known_rights_blocker_rejected():
    d = date(2026, 10, 22)
    idea = example(d)
    idea["rights_status"] = "blocked"
    assert evaluate_idea(idea, d)["status"] == "REJECT"


def test_invalid_scoring_and_old_sources():
    d = date(2026, 10, 22)
    idea = example(d)
    idea["scores"]["demand"] = 200
    with pytest.raises(ValueError):
        evaluate_idea(idea, d)
    idea = example(d)
    idea["evidence"][0]["observed_on"] = "2022-01-01"
    assert evaluate_idea(idea, d)["status"] == "HOLD"


def test_file_no_implicit_overwrite(tmp_path: Path):
    d = date(2026, 10, 22)
    src, target = tmp_path / "input.json", tmp_path / "result.json"
    src.write_text(json.dumps({"schema_version": 1, "ideas": [example(d)]}))
    first = evaluate_file(src, target, d)
    assert first["recommendations"][0]["status"] == "CANDIDATE_FOR_HUMAN_REVIEW"
    assert target.is_file()
    with pytest.raises(FileExistsError):
        evaluate_file(src, target, d)
