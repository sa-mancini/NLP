"""Notebook-friendly doctor-facing HTML rendering."""

import html
from IPython.display import HTML


class DoctorViewRenderer:
    """Render structured patient, decision, pharmaceutical, and evidence data."""

    def __init__(self, cases, gemini_results, retrieval_results):
        self.cases = {case["case_id"]: case for case in cases}
        self.gemini_results = gemini_results
        self.retrieval_results = retrieval_results

    def _patient_data(self, case):
        ehr = case.get("ehr", {})
        clinical = case.get("clinical_data", {})
        sections = [
            f"<b>età:</b> {ehr.get('age', 'n/d')}&nbsp;&nbsp;"
            f"<b>sesso:</b> {ehr.get('sex', 'n/d')}",
            f"<b>regione:</b> {ehr.get('region', 'n/d')}",
        ]

        allergies = ehr.get("allergies")
        allergy_text = ", ".join(map(str, allergies)) if isinstance(allergies, list) else str(allergies or "nessuna")
        sections.append(f"<b>allergie:</b> {html.escape(allergy_text)}")

        if ehr.get("comorbidities"):
            sections.append(f"<b>comorbidità:</b> {html.escape(', '.join(map(str, ehr['comorbidities'])))}")
        if ehr.get("pregnancy") is not None:
            sections.append(f"<b>gravidanza:</b> {'sì' if ehr['pregnancy'] else 'no'}")
        if ehr.get("gestational_age_weeks") is not None:
            sections.append(f"<b>epoca gestazionale:</b> {ehr['gestational_age_weeks']} settimane")
        if clinical.get("symptoms"):
            sections.append(f"<b>sintomi:</b> {html.escape(', '.join(map(str, clinical['symptoms'])))}")
        if clinical.get("temperature_c") is not None:
            sections.append(f"<b>temperatura:</b> {clinical['temperature_c']} °c")
        if clinical.get("symptom_duration_days") is not None:
            sections.append(f"<b>durata:</b> {clinical['symptom_duration_days']} giorni")
        if clinical.get("symptom_duration_hours") is not None:
            sections.append(f"<b>durata:</b> {clinical['symptom_duration_hours']} ore")

        centor = clinical.get("scores", {}).get("centor_mcisaac")
        if centor and centor.get("score") is not None:
            sections.append(f"<b>centor / mcisaac:</b> {centor['score']}")

        tests = clinical.get("tests")
        if isinstance(tests, dict):
            test_text = "; ".join(f"{k}: {v}" for k, v in tests.items())
            sections.append(f"<b>test:</b> {html.escape(test_text)}")
        elif isinstance(tests, list):
            sections.append(f"<b>test:</b> {html.escape('; '.join(map(str, tests)))}")
        elif tests:
            sections.append(f"<b>test:</b> {html.escape(str(tests))}")

        return "<br>".join(sections)

    @staticmethod
    def _pharmaceuticals(pharmaceuticals):
        if not pharmaceuticals:
            return "<i>nessun farmaco selezionato</i>"
        blocks = []
        for group in pharmaceuticals:
            active = html.escape(str(group.get("active_ingredient", "")))
            options = group.get("options", [])
            if not options:
                blocks.append(
                    f'<div style="margin-bottom:15px;"><b>principio attivo:</b> {active}'
                    "<br><i>nessun farmaco corrispondente trovato</i></div>"
                )
                continue
            items = "".join(
                f"<li><b>{html.escape(str(drug.get('commercial_name', '')))}</b> "
                f"— {html.escape(str(drug.get('active_ingredient', active)))}</li>"
                for drug in options
            )
            blocks.append(
                f'<div style="margin-bottom:15px;"><b>principio attivo:</b> {active}'
                f"<ul>{items}</ul></div>"
            )
        return "".join(blocks) or "<i>nessun farmaco selezionato</i>"

    @staticmethod
    def _evidence(evidence):
        if not evidence:
            return "<i>nessuna evidenza AIFA selezionata</i>"
        return "".join(
            f'<div style="margin:10px 0;"><b>pagina {html.escape(str(item.get("page", "n/d")))}</b>'
            f'<div style="margin-top:6px;font-style:italic;">{html.escape(str(item.get("text", "")))}</div></div>'
            for item in evidence
        )

    def render(self, case_id: str):
        """Return an IPython HTML object for a single case."""
        case = self.cases.get(case_id)
        result = self.gemini_results.get(case_id)
        if case is None or result is None:
            raise KeyError(f"Unknown case: {case_id}")

        decision = result.get("antibiotic_needed")
        recommendation = (
            "antibiotico raccomandato" if decision is True
            else "antibiotico non raccomandato" if decision is False
            else "decisione non determinabile"
        )
        active = html.escape(str(result.get("active_ingredient") or "nessuno"))
        reasoning = html.escape(str(result.get("reasoning") or ""))
        missing = result.get("missing_information", [])
        missing_html = (
            "<ul>" + "".join(f"<li>{html.escape(str(x))}</li>" for x in missing) + "</ul>"
            if missing else "<i>nessuna</i>"
        )

        selected_pages = result.get("evidence_pages", [])
        evidence = [
            item for item in self.retrieval_results.get(case_id, {}).get("evidence", [])
            if item.get("page") in selected_pages
        ]

        doctor_note = html.escape(str(case.get("doctor_note", "")).strip())

        return HTML(f"""
        <div style="font-family:Arial,sans-serif;max-width:1000px;margin:25px auto;
                    border:1px solid #ddd;border-radius:10px;padding:24px;">
            <h2 style="margin-top:0;">{html.escape(case_id)}</h2><hr>
            <h3>paziente</h3>
            <div style="line-height:1.7;margin-bottom:15px;">{self._patient_data(case)}</div>
            <h4 style="margin-bottom:0;">nota clinica</h4>
            <div style="white-space:pre-wrap;font-style:italic;">{doctor_note}</div>
            <hr>
            <h3>valutazione</h3>
            <p><b>decisione:</b> {html.escape(recommendation)}</p>
            <p><b>principio attivo / opzioni:</b> {active}</p>
            <h4>ragionamento</h4>
            <div style="font-weight:bold;">{reasoning}</div>
            <h4>informazioni mancanti</h4>
            <div>{missing_html}</div><hr>
            <h3>farmaci corrispondenti</h3>
            {self._pharmaceuticals(result.get("pharmaceuticals", []))}
            <hr>
            <h3>evidenza AIFA utilizzata</h3>
            <p><b>pagine selezionate:</b> {", ".join(map(str, selected_pages))}</p>
            {self._evidence(evidence)}
        </div>
        """)
