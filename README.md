# Retrieval-Augmented Clinical Decision Support for Antibiotic Prescribing

## Report and presentation

- [Report](report.pdf)
- [Presentation](presentation.pdf)

## Project structure

```text
NLP/
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

Download the [AIFA AWaRe guideline PDF](https://www.aifa.gov.it/documents/20142/1811463/Manuale_antibiotici_AWaRe.pdf) and run:

```bash
python build_vectorstore.py path/to/Manuale_antibiotici_AWaRe.pdf
```

The default output is `data/e5_vectorstore/`.

The repository already contains the precomputed vectorstore, so rebuilding it is not necessary to run the demo notebook.

## 2. Run the complete pipeline

```bash
python main.py
```

Results are written to `results/gemini_results.json`.

### Gemini API warning

The Gemini API can intermittently return `503 UNAVAILABLE` errors when the selected model is experiencing high demand. This may interrupt the pipeline even when the rest of the project is working correctly.

For this reason, the repository already includes the precomputed Gemini results.

## 3. Demo notebook 

The demo notebook loads the precomputed results from `results/gemini_results.json` and displays the results for demonstration, inspection, and visualization.  

## Notes

- The Gemini API key is read from the `GEMINI_API_KEY` environment variable.
- The pharmaceutical matching stage currently uses the AIFA active-ingredient table (`Classe_A_per_principio_attivo_31-12-2025.csv`). The commercial-name and package tables are loaded for completeness/future extensions but are not required by the current matching function.
- GPU is preferred for the multilingual E5 embedding model. If running without CUDA, change `device` in `src/rag.py` to `"cpu"`.
