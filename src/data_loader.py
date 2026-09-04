"""Data loading utilities."""

from pathlib import Path
from typing import Any
import json

from data.synthetic_cases import synthetic_cases


def load_synthetic_cases() -> list[dict[str, Any]]:
    """Return the synthetic patient dataset."""
    return synthetic_cases


def save_json(data: Any, path: str | Path) -> None:
    """Save JSON data with UTF-8 encoding."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_json(path: str | Path) -> Any:
    """Load JSON data from disk."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
