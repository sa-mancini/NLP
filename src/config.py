"""Configuration and constants for the project."""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for retrieval, LLM inference, and data paths."""

    embedding_model: str = "intfloat/multilingual-e5-base"
    llm_model: str = "gemini-3.6-flash"
    chunk_size: int = 900
    chunk_overlap: int = 150
    max_results: int = 15
    max_unique_pages: int = 10
    max_distance: float = 0.30
    guideline_start_page: int = 35
    guideline_end_page: int = 240
    vectorstore_path: Path = Path("data/e5_vectorstore")
    results_path: Path = Path("results/gemini_results.json")

    @property
    def gemini_api_key(self) -> str | None:
        """Return the Gemini API key from the environment."""
        return os.getenv("GEMINI_API_KEY")


URL_AIFA_GUIDELINES = (
    "https://www.aifa.gov.it/documents/20142/1811463/"
    "Manuale_antibiotici_AWaRe.pdf"
)

URL_DATI2024 = (
    "https://www.aifa.gov.it/documents/20142/847578/"
    "dati2024_04.12.2025.csv"
)

AIFA_TABLE_URLS = {
    "classe_a_principio_attivo": (
        "https://www.aifa.gov.it/documents/20142/3789005/"
        "Classe_A_per_principio_attivo_31-12-2025.csv"
    ),
    "classe_a_nome_commerciale": (
        "https://www.aifa.gov.it/documents/20142/3789005/"
        "Classe_A_per_nome_commerciale_31-12-2025.csv"
    ),
    "pa_confezioni": "https://drive.aifa.gov.it/farmaci/PA_confezioni.csv",
}
