"""Run the antibiotic prescribing RAG pipeline.

Set GEMINI_API_KEY in the environment before running.
The AIFA guideline PDF and vectorstore are expected to be available locally.
"""

import argparse
from pathlib import Path

from data.synthetic_cases import synthetic_cases
from src.config import Settings
from src.data_loader import save_json
from src.llm_reasoning import GeminiReasoner
from src.pharmaceutical import load_aifa_tables, match_results_to_pharmaceuticals
from src.rag import create_embeddings, load_vectorstore, GuidelineRetriever
from src.regional_pressure import (
    build_pressure_maps,
    calculate_regional_pressure,
    load_aifa_consumption_data,
)
from src.pipeline import ClinicalDecisionPipeline


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vectorstore", type=Path, default=Settings().vectorstore_path)
    parser.add_argument("--output", type=Path, default=Settings().results_path)
    return parser.parse_args()


def main():
    args = parse_args()
    settings = Settings(vectorstore_path=args.vectorstore, results_path=args.output)

    embeddings = create_embeddings(settings.embedding_model)
    vectorstore = load_vectorstore(settings.vectorstore_path, embeddings)
    retriever = GuidelineRetriever(
        vectorstore,
        max_results=settings.max_results,
        max_unique_pages=settings.max_unique_pages,
        max_distance=settings.max_distance,
    )

    consumption = load_aifa_consumption_data()
    pressure = calculate_regional_pressure(consumption)
    region_pressure, region_pressure_level = build_pressure_maps(pressure)

    reasoner = GeminiReasoner(
        api_key=settings.gemini_api_key,
        model=settings.llm_model,
    )

    pipeline = ClinicalDecisionPipeline(
        retriever,
        reasoner,
        region_pressure,
        region_pressure_level,
    )
    retrieval_results, packages, gemini_results = pipeline.run(synthetic_cases)

    tables = load_aifa_tables()
    gemini_results = match_results_to_pharmaceuticals(
        gemini_results,
        tables["classe_a_principio_attivo"],
    )

    # Keep retrieval/evidence information with the saved experiment output.
    for case_id, result in gemini_results.items():
        result["retrieval"] = retrieval_results[case_id]

    save_json(gemini_results, settings.results_path)
    print(f"Saved results to {settings.results_path}")


if __name__ == "__main__":
    main()
