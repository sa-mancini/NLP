"""AIFA guideline ingestion, embedding, vectorstore, and retrieval."""

from pathlib import Path
from typing import Any

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_guideline_pages(
    pdf_path: str | Path,
    start_page: int = 35,
    end_page: int = 240,
):
    """Load and retain the relevant AIFA PDF pages, preserving PDF page numbers."""
    loader = PyMuPDFLoader(str(pdf_path))
    all_documents = loader.load()
    documents = all_documents[start_page - 1:end_page]

    for doc in documents:
        doc.metadata["pdf_page"] = doc.metadata["page"] + 1

    return documents


def split_documents(documents, chunk_size: int = 900, chunk_overlap: int = 150):
    """Split guideline pages into overlapping text chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def create_embeddings(model_name: str = "intfloat/multilingual-e5-base"):
    """Create normalized multilingual E5 embeddings."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cuda"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore(chunks, embeddings):
    """Build a FAISS vectorstore using E5 passage prefixes."""
    e5_documents = []
    for doc in chunks:
        new_doc = doc.model_copy()
        new_doc.page_content = "passage: " + doc.page_content
        e5_documents.append(new_doc)

    return FAISS.from_documents(e5_documents, embeddings)


def save_vectorstore(vectorstore, path: str | Path) -> None:
    """Persist a FAISS vectorstore locally."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(path))


def load_vectorstore(path: str | Path, embeddings):
    """Load a persisted FAISS vectorstore."""
    return FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def build_rag_query(case: dict[str, Any]) -> str:
    """Construct a patient-aware retrieval query."""
    ehr = case.get("ehr", {})
    clinical_data = case.get("clinical_data", {})
    parts = []

    doctor_note = case.get("doctor_note", "")
    if doctor_note:
        parts.append(doctor_note)

    age = ehr.get("age")
    if age is not None:
        parts.append("bambini" if age < 18 else "adulti")

    symptoms = clinical_data.get("symptoms", [])
    if symptoms:
        parts.append(", ".join(symptoms))

    centor = clinical_data.get("scores", {}).get("centor_mcisaac")
    if centor is not None and centor.get("score") is not None:
        parts.append("Centor / McIsaac")

    if ehr.get("pregnancy") is True:
        parts.append("gravidanza")

    tests = clinical_data.get("tests")
    if isinstance(tests, dict):
        parts.extend(tests.keys())
    elif isinstance(tests, list):
        parts.extend(tests)
    elif isinstance(tests, str):
        parts.append(tests)

    parts.extend([
        "trattamento antibiotico empirico",
        "considerazioni cliniche trattamento antibiotico",
        "durata del trattamento antibiotico",
    ])
    return "\n".join(parts)


class GuidelineRetriever:
    """Retrieve unique, sufficiently similar AIFA guideline pages."""

    def __init__(
        self,
        vectorstore,
        max_results: int = 15,
        max_unique_pages: int = 10,
        max_distance: float = 0.30,
    ):
        self.vectorstore = vectorstore
        self.max_results = max_results
        self.max_unique_pages = max_unique_pages
        self.max_distance = max_distance

    def retrieve(self, case: dict[str, Any]) -> dict[str, Any]:
        """Retrieve guideline evidence for one patient case."""
        query = build_rag_query(case)
        results = self.vectorstore.similarity_search_with_score(
            "query: " + query,
            k=self.max_results,
        )

        evidence = []
        seen_pages = set()

        for doc, distance in results:
            distance = float(distance)
            if distance > self.max_distance:
                continue

            page = doc.metadata.get(
                "pdf_page",
                doc.metadata.get("page", "N/D"),
            )
            if page in seen_pages:
                continue

            seen_pages.add(page)
            evidence.append({
                "page": page,
                "distance": distance,
                "text": doc.page_content,
            })

            if len(evidence) >= self.max_unique_pages:
                break

        return {"query": query, "evidence": evidence}
