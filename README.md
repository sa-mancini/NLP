# Retrieval-Augmented Clinical Decision Support for Antibiotic Prescribing

Modular Python implementation of the project *Retrieval-Augmented Clinical Decision Support for Antibiotic Prescribing: Integrating LLM Reasoning with AIFA Guidelines and Pharmaceutical Data*.

## Project structure

```text
antibiotics_nlp_project/
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── rag.py
│   ├── regional_pressure.py
│   ├── llm_reasoning.py
│   ├── pharmaceutical.py
│   ├── pipeline.py
│   └── presentation.py
├── data/
│   └── synthetic_cases.py
├── notebooks/
│   └── demo.ipynb
├── results/
├── build_vectorstore.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_KEY"
```

On Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

## 1. Build the guideline vectorstore

Download the AIFA AWaRe guideline PDF and run:

```bash
python build_vectorstore.py path/to/Manuale_antibiotici_AWaRe.pdf
```

The default output is `data/e5_vectorstore/`.

## 2. Run the complete pipeline

```bash
python main.py
```

Results are written to `results/gemini_results.json`.

## 3. Notebook usage

The notebook is intended only for demonstration, inspection, and visualization. It imports the reusable components from `src/` rather than containing the application logic.

## Notes

- The Gemini API key is read from the `GEMINI_API_KEY` environment variable.
- The pharmaceutical matching stage currently uses the AIFA active-ingredient table (`Classe_A_per_principio_attivo_31-12-2025.csv`). The commercial-name and package tables are loaded for completeness/future extensions but are not required by the current matching function.
- GPU is preferred for the multilingual E5 embedding model. If running without CUDA, change `device` in `src/rag.py` to `"cpu"`.
