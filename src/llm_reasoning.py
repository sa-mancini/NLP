"""Gemini prompt construction and clinical reasoning."""

import json
from typing import Any

from google import genai


def build_gemini_prompt(package):

    patient_text = json.dumps(
        package["patient"],
        ensure_ascii=False,
        indent=2
    )

    guideline_text = ""

    for i, guideline in enumerate(
        package["guideline_evidence"],
        start=1
    ):
        guideline_text += f"""
==================================================
PASSAGGIO RECUPERATO {i}
PAGINA PDF: {guideline['page']}
DISTANZA RETRIEVAL: {guideline['retrieval_distance']}

{guideline['text']}
"""

    return f"""
SEI UN ASSISTENTE DI RICERCA CLINICA.

DEVI APPLICARE LE LINEE GUIDA RECUPERATE AL CASO
CLINICO SPECIFICO FORNITO.

PUOI UTILIZZARE ESCLUSIVAMENTE:

1. dati clinici del paziente;
2. criteri clinici già calcolati;
3. raccomandazioni contenute nei passaggi delle
   linee guida recuperati.

NON utilizzare conoscenze mediche esterne.

==================================================
REGOLA FONDAMENTALE
==================================================

NON devi decidere l'esito sulla base della frase più
generica, più prudente o più frequentemente ripetuta
nei passaggi recuperati.

Devi identificare LA RACCOMANDAZIONE DELLA LINEA GUIDA
PIÙ DIRETTAMENTE APPLICABILE AL PROFILO CLINICO
SPECIFICO DEL PAZIENTE.

Una raccomandazione generale NON deve sostituire una
raccomandazione più specifica applicabile al caso.

==================================================
DATI DEL PAZIENTE
==================================================

{patient_text}

==================================================
PASSAGGI DELLE LINEE GUIDA RECUPERATI
==================================================

{guideline_text}

==================================================
PROCEDURA OBBLIGATORIA
==================================================

Prima di determinare antibiotic_needed, esegui
mentalmente questi passaggi:

STEP 1 — IDENTIFICA IL PROFILO CLINICO

Identifica:

- condizione;
- età;
- sintomi;
- segni obiettivi;
- risultati clinici;
- punteggi disponibili;
- fattori di rischio;
- gravidanza, quando rilevante;
- allergie;
- precedenti antibiotici;
- comorbidità;
- eventuale contesto regionale.

Non ignorare informazioni cliniche presenti nel caso.

--------------------------------------------------

STEP 2 — IDENTIFICA I CRITERI DECISIONALI

Cerca nei passaggi recuperati:

- soglie;
- score;
- criteri diagnostici;
- algoritmi;
- indicazioni al trattamento;
- indicazioni alla non prescrizione;
- eccezioni;
- condizioni specifiche;
- raccomandazioni specifiche per sottogruppi
  di pazienti.

--------------------------------------------------

STEP 3 — COLLEGA PAZIENTE E LINEA GUIDA

Confronta esplicitamente i dati del paziente con
i criteri della linea guida.

Esempio:

PAZIENTE:
Centor/McIsaac = X

LINEA GUIDA:
per score X la raccomandazione è Y

CONCLUSIONE:
il paziente rientra nella categoria Y.

Devi ragionare in questo modo anche quando il
criterio non è uno score ma una combinazione di
sintomi, segni o fattori clinici.

--------------------------------------------------

STEP 4 — SCEGLI LA RACCOMANDAZIONE APPLICABILE

Se sono presenti più affermazioni nella linea guida,
scegli quella che descrive più precisamente il caso.

PRIORITÀ:

1. raccomandazione specifica per il profilo del paziente;
2. criterio/soglia direttamente applicabile;
3. raccomandazione generale sulla condizione.

NON utilizzare una raccomandazione generale per
contraddire una raccomandazione specifica senza
una motivazione esplicita presente nella linea guida.

--------------------------------------------------

STEP 5 — DATI REGIONALI / RESISTENZA

NON assumere che un dato regionale sia necessario.

NON richiedere automaticamente:

- resistenza antimicrobica;
- antibiogramma;
- prevalenza di resistenze;
- prevalenza regionale;
- pressione antibiotica;
- prevalenza della febbre reumatica.

Usa questi dati SOLO se una raccomandazione
specifica della linea guida li identifica come
criterio necessario per decidere se prescrivere
l'antibiotico nel profilo clinico considerato.

La semplice presenza di una frase riguardante
resistenza, prevalenza o pressione antibiotica
NON rende automaticamente tale informazione
necessaria.

--------------------------------------------------

STEP 6 — INFORMAZIONI MANCANTI

Non restituire null solo perché manca un'informazione
che non è necessaria per applicare la raccomandazione.

Usa null SOLO quando:

- la linea guida contiene una regola decisionale
  applicabile;
- ma manca effettivamente un'informazione necessaria
  per sapere in quale categoria ricade il paziente.

Se tutti i criteri necessari sono presenti,
devi produrre true oppure false.

==================================================
CASO SPECIALE: FARINGITE
==================================================

Per la faringite, presta particolare attenzione a:

- Centor/McIsaac;
- febbre >38°C;
- assenza/presenza di tosse;
- essudato tonsillare;
- linfonodi cervicali anteriori dolenti;
- età;
- eventuali soglie o categorie definite dalla
  linea guida.

Se il punteggio Centor/McIsaac è già presente nei dati
del paziente, UTILIZZALO.

Non ignorare il punteggio solo perché i singoli
elementi clinici sono descritti separatamente.

Esempio:

Centor/McIsaac = 4

non deve essere trattato come se il paziente avesse
Centor = 0 semplicemente perché nei passaggi recuperati
compare una frase generale sulla faringite.

==================================================
CASO SPECIALE: INFEZIONE DELLE VIE URINARIE
==================================================

Per le infezioni urinarie considera, quando presenti:

- disuria;
- frequenza;
- urgenza;
- febbre;
- brividi;
- dolore al fianco;
- sintomi sistemici;
- gravidanza;
- sesso;
- ricorrenza;
- comorbidità;
- altri criteri specifici presenti nella linea guida.

Determina innanzitutto quale categoria clinica
descrive il paziente e successivamente applica
la raccomandazione corrispondente.

==================================================
CONTROLLO DI COERENZA
==================================================

Prima dell'output verifica:

1. Qual è il principale criterio clinico del paziente?
2. Quale passaggio della linea guida contiene la
   raccomandazione applicabile a quel criterio?
3. Il paziente soddisfa quel criterio?
4. Esiste un'eccezione esplicitamente descritta
   dalla linea guida?
5. Sto richiedendo informazioni che la linea guida
   non richiede?
6. Sto dando più peso a una frase generale rispetto
   a una raccomandazione specifica?

Se non puoi identificare una raccomandazione
applicabile, usa null.

Se puoi identificarla e il paziente soddisfa i criteri,
usa true o false.

==================================================
PRINCIPIO ATTIVO
==================================================

Se antibiotic_needed = true:

indica il principio attivo SOLO se è esplicitamente
riportato nei passaggi recuperati.

Altrimenti:

active_ingredient = null

Non inventare:

- principi attivi;
- dosaggi;
- durata;
- alternative;
- terapie.

==================================================
EVIDENZA
==================================================

evidence_pages deve contenere SOLO le pagine dei
passaggi effettivamente utilizzati per la decisione.

La distanza del retrieval NON è evidenza clinica.

==================================================
OUTPUT OBBLIGATORIO
==================================================

Rispondi esclusivamente con JSON valido:

{{
    "antibiotic_needed": true,
    "active_ingredient": null,
    "reasoning": "collegamento esplicito tra dati clinici del paziente e raccomandazione applicabile della linea guida",
    "evidence_pages": [],
    "missing_information": [],
    "evidence_sufficient": true
}}

REGOLE FINALI:

- true = raccomandazione antibiotica applicabile
  e soddisfatta dal paziente.
- false = raccomandazione di non utilizzare antibiotici
  applicabile e soddisfatta dal paziente.
- null = manca una informazione NECESSARIA.
- I dati clinici del paziente devono essere utilizzati
  attivamente.
- I criteri clinici e gli score devono essere applicati.
- Una frase generale non deve dominare una regola
  specifica applicabile.
- Non richiedere automaticamente dati di resistenza.
- Non usare conoscenze esterne.
- Non inventare informazioni.
"""

class GeminiReasoner:
    """Run Gemini on evidence packages and normalize its JSON response."""

    def __init__(self, api_key: str, model: str = "gemini-3.6-flash"):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required.")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def run(self, package: dict[str, Any]) -> dict[str, Any]:
        """Generate and parse one guideline-grounded clinical decision."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=build_gemini_prompt(package),
        )
        raw_text = response.text
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = None

        return {
            "response_text": raw_text,
            "antibiotic_needed": parsed.get("antibiotic_needed") if parsed else None,
            "active_ingredient": parsed.get("active_ingredient") if parsed else None,
            "reasoning": parsed.get("reasoning") if parsed else None,
            "evidence_pages": parsed.get("evidence_pages", []) if parsed else [],
            "missing_information": parsed.get("missing_information", []) if parsed else [],
            "evidence_sufficient": parsed.get("evidence_sufficient", False) if parsed else False,
            "evidence_package": package,
        }
