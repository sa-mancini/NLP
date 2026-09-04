"""Build the persistent AIFA E5 vectorstore from the guideline PDF."""

import argparse
from pathlib import Path

from src.config import Settings
from src.rag import (
    build_vectorstore,
    create_embeddings,
    load_guideline_pages,
    save_vectorstore,
    split_documents,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, help="Path to the AIFA AWaRe PDF")
    parser.add_argument(
        "--output",
        type=Path,
        default=Settings().vectorstore_path,
    )
    args = parser.parse_args()

    settings = Settings()
    documents = load_guideline_pages(
        args.pdf,
        settings.guideline_start_page,
        settings.guideline_end_page,
    )
    chunks = split_documents(
        documents,
        settings.chunk_size,
        settings.chunk_overlap,
    )
    embeddings = create_embeddings(settings.embedding_model)
    vectorstore = build_vectorstore(chunks, embeddings)
    save_vectorstore(vectorstore, args.output)

    print(f"Created vectorstore at: {args.output}")
    print(f"Pages: {len(documents)} | Chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
