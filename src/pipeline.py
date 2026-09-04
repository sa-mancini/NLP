"""End-to-end orchestration of the clinical decision support pipeline."""

from typing import Any

from .llm_reasoning import GeminiReasoner
from .rag import GuidelineRetriever
from .regional_pressure import build_pressure_maps


def build_patient_context(
    case: dict[str, Any],
    region_pressure: dict,
    region_pressure_level: dict,
) -> dict[str, Any]:
    """Combine patient data with regional antibiotic pressure."""
    region = case["ehr"].get("region")
    return {
        "case_id": case["case_id"],
        "doctor_note": case["doctor_note"],
        "ehr": case["ehr"],
        "clinical_features": case.get("clinical_data", {}),
        "regional_context": {
            "region": region,
            "antibiotic_pressure": region_pressure.get(region),
            "antibiotic_pressure_level": region_pressure_level.get(region),
        },
    }


def build_evidence_package(
    case: dict[str, Any],
    retrieval: dict[str, Any],
    region_pressure: dict,
    region_pressure_level: dict,
) -> dict[str, Any]:
    """Build the complete context supplied to the LLM."""
    return {
        "patient": build_patient_context(
            case, region_pressure, region_pressure_level
        ),
        "guideline_retrieval_query": retrieval["query"],
        "guideline_evidence": [
            {
                "page": item["page"],
                "retrieval_distance": item["distance"],
                "text": item["text"],
            }
            for item in retrieval["evidence"]
        ],
    }


class ClinicalDecisionPipeline:
    """Coordinate retrieval, evidence packaging, LLM reasoning, and matching."""

    def __init__(
        self,
        retriever: GuidelineRetriever,
        reasoner: GeminiReasoner,
        region_pressure: dict,
        region_pressure_level: dict,
    ):
        self.retriever = retriever
        self.reasoner = reasoner
        self.region_pressure = region_pressure
        self.region_pressure_level = region_pressure_level

    def retrieve_all(self, cases):
        """Retrieve guideline evidence for every case."""
        return {
            case["case_id"]: self.retriever.retrieve(case)
            for case in cases
        }

    def build_packages(self, cases, retrieval_results):
        """Create LLM evidence packages for every case."""
        return {
            case["case_id"]: build_evidence_package(
                case,
                retrieval_results[case["case_id"]],
                self.region_pressure,
                self.region_pressure_level,
            )
            for case in cases
        }

    def run(self, cases):
        """Run retrieval and LLM reasoning over all cases."""
        retrieval_results = self.retrieve_all(cases)
        packages = self.build_packages(cases, retrieval_results)
        results = {}
        for case in cases:
            case_id = case["case_id"]
            results[case_id] = self.reasoner.run(packages[case_id])
        return retrieval_results, packages, results
