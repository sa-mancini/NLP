"""Evaluation helpers for synthetic clinical cases."""

from collections import Counter
from typing import Any


def evaluate_decisions(
    results: dict[str, dict[str, Any]],
    expected: dict[str, bool | None],
) -> dict[str, Any]:
    """Compare predicted antibiotic decisions with expected labels."""
    rows = []
    for case_id, expected_value in expected.items():
        predicted = results.get(case_id, {}).get("antibiotic_needed")
        rows.append({
            "case_id": case_id,
            "expected": expected_value,
            "predicted": predicted,
            "correct": predicted == expected_value,
        })

    comparable = [row for row in rows if row["expected"] is not None]
    accuracy = (
        sum(row["correct"] for row in comparable) / len(comparable)
        if comparable else None
    )
    return {"cases": rows, "accuracy": accuracy}


def summarize_decisions(results: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Count true, false, and indeterminate model decisions."""
    counts = Counter(
        "true" if r.get("antibiotic_needed") is True
        else "false" if r.get("antibiotic_needed") is False
        else "null"
        for r in results.values()
    )
    return dict(counts)
