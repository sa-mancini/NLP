"""Regional antibiotic consumption and pressure calculation."""

from io import StringIO
import pandas as pd
import requests

from .config import URL_DATI2024


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/csv,text/plain,*/*",
}


def normalize_region(region: str) -> str:
    """Normalize region names for matching with patient records."""
    return str(region).strip().title().replace("-", " ")


def load_aifa_consumption_data(url: str = URL_DATI2024) -> pd.DataFrame:
    """Download and parse the AIFA 2024 antibiotic consumption dataset."""
    response = requests.get(
        url,
        headers=HEADERS,
        verify=False,
        timeout=60,
    )
    response.raise_for_status()
    return pd.read_csv(
        StringIO(response.text),
        sep="|",
        engine="python",
        on_bad_lines="skip",
    )


def calculate_regional_pressure(dati2024: pd.DataFrame) -> pd.DataFrame:
    """Compute normalized antibiotic package usage and tertile pressure."""
    data = dati2024.copy()
    for col in [
        "numero_confezioni_traccia",
        "numero_confezioni_convenzionata",
    ]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    abx = data[data["atc1"] == "J"]
    pressure = abx.groupby("regione")[
        ["numero_confezioni_traccia", "numero_confezioni_convenzionata"]
    ].sum()

    pressure["usage"] = (
        pressure["numero_confezioni_traccia"]
        + pressure["numero_confezioni_convenzionata"]
    )

    usage_min = pressure["usage"].min()
    usage_max = pressure["usage"].max()

    if usage_max != usage_min:
        pressure["pressure"] = (
            (pressure["usage"] - usage_min)
            / (usage_max - usage_min)
        )
    else:
        pressure["pressure"] = 0

    pressure["pressure_level"] = pd.qcut(
        pressure["pressure"],
        q=3,
        labels=["low", "medium", "high"],
        duplicates="drop",
    )

    pressure.index = [normalize_region(x) for x in pressure.index]
    return pressure


def build_pressure_maps(pressure: pd.DataFrame):
    """Return region-to-pressure and region-to-level mappings."""
    return (
        pressure["pressure"].to_dict(),
        pressure["pressure_level"].astype(str).to_dict(),
    )
