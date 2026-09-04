"""AIFA pharmaceutical matching utilities."""

import re
import pandas as pd
import requests
from io import StringIO

from .config import AIFA_TABLE_URLS


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/csv,text/plain,*/*",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


def download_text(url: str) -> str:
    """Download a text/CSV resource."""
    response = requests.get(
        url, headers=HEADERS, verify=False, timeout=60
    )
    response.raise_for_status()
    return response.text


def smart_read_csv(text: str) -> pd.DataFrame:
    """Parse AIFA CSV content while tolerating common separators."""
    for sep in [";", ",", "\t"]:
        try:
            df = pd.read_csv(
                StringIO(text),
                sep=sep,
                engine="python",
                on_bad_lines="skip",
            )
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    return pd.read_csv(
        StringIO(text), sep=None, engine="python", on_bad_lines="skip"
    )


def load_aifa_tables(urls: dict[str, str] | None = None):
    """Load AIFA pharmaceutical tables.

    The matching pipeline currently uses only the active-ingredient table.
    The commercial-name and package tables are loaded for completeness and
    future extensions.
    """
    urls = urls or AIFA_TABLE_URLS
    dataframes = {}
    for name, url in urls.items():
        dataframes[name] = smart_read_csv(download_text(url))
    return dataframes


def normalize_text(value) -> str:
    """Normalize accents, whitespace, separators, and case."""
    if pd.isna(value):
        return ""
    value = str(value).strip().lower()
    replacements = {"à": "a", "è": "e", "é": "e", "ì": "i", "ò": "o", "ù": "u"}
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = value.replace("+", "/")
    value = re.sub(r"\s*/\s*", "/", value)
    return " ".join(value.split())


def extract_commercial_name(denomination) -> str:
    """Extract the commercial product name from an AIFA denomination field."""
    if pd.isna(denomination):
        return ""
    denomination = str(denomination).strip()
    if "*" in denomination:
        return denomination.split("*", 1)[0].strip()
    return denomination.split()[0].strip()


def split_active_ingredients(active_ingredient: str) -> list[str]:
    """Split alternative or combination active ingredients."""
    if not active_ingredient:
        return []
    text = str(active_ingredient).strip().replace("(", "").replace(")", "")
    parts = re.split(r"\s+\bo\b\s+", text, flags=re.IGNORECASE)
    alternatives = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        for slash_part in re.split(r"\s+/\s+", part):
            slash_part = re.sub(r"\s*\+\s*", "/", slash_part.strip())
            if slash_part:
                alternatives.append(slash_part)
    return alternatives


def find_pharmaceuticals(active_ingredient: str, df_pa: pd.DataFrame) -> list[dict]:
    """Find commercial names corresponding to an active ingredient."""
    if not active_ingredient:
        return []

    target = normalize_text(active_ingredient)
    if not target:
        return []

    df = df_pa.copy()
    df["_active_normalized"] = df["Principio Attivo"].apply(normalize_text)

    matches = df[df["_active_normalized"] == target].copy()
    if matches.empty:
        matches = df[
            df["_active_normalized"].str.contains(target, na=False, regex=False)
        ].copy()
    if matches.empty:
        matches = df[
            df["_active_normalized"].apply(
                lambda value: isinstance(value, str)
                and value != ""
                and value in target
            )
        ].copy()
    if matches.empty:
        return []

    matches["commercial_name"] = matches[
        "Denominazione e Confezione"
    ].apply(extract_commercial_name)
    matches = matches[matches["commercial_name"].str.len() > 0].copy()
    if matches.empty:
        return []

    matches["_commercial_normalized"] = matches["commercial_name"].apply(normalize_text)
    unique_matches = matches[
        ["commercial_name", "Principio Attivo", "_commercial_normalized", "_active_normalized"]
    ].drop_duplicates(
        subset=["_commercial_normalized", "_active_normalized"]
    )

    return [
        {
            "commercial_name": row["commercial_name"],
            "active_ingredient": row["Principio Attivo"],
        }
        for _, row in unique_matches.iterrows()
    ]


def match_results_to_pharmaceuticals(gemini_results: dict, df_pa: pd.DataFrame) -> dict:
    """Add pharmaceutical matches to all positive Gemini decisions."""
    for result in gemini_results.values():
        result["pharmaceuticals"] = []
        if result.get("antibiotic_needed") is True and result.get("active_ingredient"):
            for ingredient in split_active_ingredients(result["active_ingredient"]):
                result["pharmaceuticals"].append({
                    "active_ingredient": ingredient,
                    "options": find_pharmaceuticals(ingredient, df_pa),
                })
    return gemini_results
