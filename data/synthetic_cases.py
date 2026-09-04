"""Synthetic patient cases used for evaluation."""

synthetic_cases = [

    # ========================================================
    # FARINGITE 1 — TRUE
    # ========================================================

    {
        "case_id": "FAR_001",

        "doctor_note": """
Paziente di 12 anni presenta faringite con mal di gola
intenso e febbre da 2 giorni.
Riferisce dolore importante alla deglutizione.
Nega tosse e rinorrea.
Sono presenti essudato tonsillare bilaterale e linfonodi
cervicali anteriori dolenti.
""",

        "ehr": {
            "age": 12,
            "sex": "maschio",
            "region": "Molise",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "amoxicillina",
                    "indication": "otite media acuta"
                }
            ],
            "comorbidities": []
        },

        "clinical_data": {
            "symptoms": [
                "mal di gola",
                "febbre",
                "odinofagia"
            ],
            "symptom_duration_days": 2,
            "temperature_c": 39.1,
            "negative_symptoms": [
                "tosse",
                "rinorrea"
            ],
            "scores": {
                "centor_mcisaac": {
                    "tonsillar_exudate": True,
                    "tender_anterior_cervical_nodes": True,
                    "fever_over_38": True,
                    "absence_of_cough": True,
                    "age": 12,
                    "score": 5
                }
            }
        }
    },


    # ========================================================
    # FARINGITE 2 — FALSE
    # ========================================================

    {
        "case_id": "FAR_002",

        "doctor_note": """
Paziente di 28 anni presenta faringite con mal di gola
da 3 giorni associato a tosse, rinorrea e raucedine.
Riferisce lieve fastidio alla deglutizione.
Non riferisce febbre significativa.
Non sono presenti essudato tonsillare né linfonodi
cervicali anteriori dolenti.
""",

        "ehr": {
            "age": 28,
            "sex": "femmina",
            "region": "Lombardia",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "fosfomicina",
                    "indication": "infezione delle vie urinarie"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "mal di gola",
                "tosse",
                "rinorrea",
                "raucedine"
            ],
            "symptom_duration_days": 3,
            "temperature_c": 37.4,
            "negative_symptoms": [
                "febbre significativa",
                "odinofagia intensa"
            ],
            "scores": {
                "centor_mcisaac": {
                    "tonsillar_exudate": False,
                    "tender_anterior_cervical_nodes": False,
                    "fever_over_38": False,
                    "absence_of_cough": False,
                    "age": 28,
                    "score": 0
                }
            }
        }
    },


    # ========================================================
    # FARINGITE 3 — TRUE
    # ========================================================

    {
        "case_id": "FAR_003",

        "doctor_note": """
Paziente di 39 anni presenta faringite con febbre e
odinofagia da 3 giorni.
Riferisce dolore alla deglutizione.
Nega tosse e rinorrea.
Sono presenti essudato tonsillare bilaterale e linfonodi
cervicali anteriori dolenti.
""",

        "ehr": {
            "age": 39,
            "sex": "femmina",
            "region": "Lombardia",
            "allergies": [
                {
                    "drug": "penicillina",
                    "reaction": "orticaria"
                }
            ],
            "previous_antibiotics": [
                {
                    "drug": "azitromicina",
                    "indication": "infezione respiratoria"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "febbre",
                "odinofagia",
                "mal di gola"
            ],
            "symptom_duration_days": 3,
            "temperature_c": 38.6,
            "negative_symptoms": [
                "tosse",
                "rinorrea"
            ],
            "scores": {
                "centor_mcisaac": {
                    "tonsillar_exudate": True,
                    "tender_anterior_cervical_nodes": True,
                    "fever_over_38": True,
                    "absence_of_cough": True,
                    "age": 39,
                    "score": 4
                }
            }
        }
    },


    # ========================================================
    # FARINGITE 4 — FALSE
    # ========================================================

    {
        "case_id": "FAR_004",

        "doctor_note": """
Paziente di 67 anni presenta faringite con irritazione
alla gola da 2 giorni associata a tosse produttiva e rinorrea.
Riferisce lieve fastidio alla deglutizione.
Non riferisce febbre significativa.
Non sono presenti essudato tonsillare né linfonodi
cervicali anteriori dolenti.
""",

        "ehr": {
            "age": 67,
            "sex": "femmina",
            "region": "Veneto",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "amoxicillina/acido clavulanico",
                    "indication": "sinusite batterica"
                }
            ],
            "comorbidities": [
                "diabete mellito tipo 2"
            ],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "irritazione della gola",
                "tosse produttiva",
                "rinorrea"
            ],
            "symptom_duration_days": 2,
            "temperature_c": 37.2,
            "negative_symptoms": [
                "febbre",
                "disfagia importante"
            ],
            "scores": {
                "centor_mcisaac": {
                    "tonsillar_exudate": False,
                    "tender_anterior_cervical_nodes": False,
                    "fever_over_38": False,
                    "absence_of_cough": False,
                    "age": 67,
                    "score": 0
                }
            }
        }
    },


    # ========================================================
    # FARINGITE 5 — EDGE
    # ========================================================

    {
        "case_id": "FAR_005",

        "doctor_note": """
Paziente di 32 anni presenta faringite con mal di gola
e febbre da 2 giorni.
Riferisce dolore alla deglutizione.
Nega tosse e rinorrea.
È presente essudato tonsillare.
I linfonodi cervicali anteriori non risultano chiaramente
dolenti.
""",

        "ehr": {
            "age": 32,
            "sex": "maschio",
            "region": "Toscana",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "azitromicina",
                    "indication": "bronchite"
                }
            ],
            "comorbidities": []
        },

        "clinical_data": {
            "symptoms": [
                "mal di gola",
                "febbre",
                "odinofagia"
            ],
            "symptom_duration_days": 2,
            "temperature_c": 38.2,
            "negative_symptoms": [
                "tosse",
                "rinorrea"
            ],
            "scores": {
                "centor_mcisaac": {
                    "tonsillar_exudate": True,
                    "tender_anterior_cervical_nodes": False,
                    "fever_over_38": True,
                    "absence_of_cough": True,
                    "age": 32,
                    "score": 3
                }
            }
        }
    },


    # ========================================================
    # UTI 1 — TRUE
    # typical acute lower UTI
    # ========================================================

    {
        "case_id": "UTI_001",

        "doctor_note": """
Paziente di 26 anni presenta da 2 giorni disuria acuta,
aumento della frequenza della minzione e urgenza minzionale.
Riferisce lieve dolore e disagio nella parte inferiore
dell'addome.
Non riferisce altri disturbi genito-urinari.
Il quadro viene valutato nel contesto di una sospetta
infezione delle vie urinarie inferiori.
""",

        "ehr": {
            "age": 26,
            "sex": "femmina",
            "region": "Toscana",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "nitrofurantoina",
                    "indication": "infezione delle vie urinarie"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "disuria acuta",
                "aumento della frequenza della minzione",
                "urgenza minzionale",
                "dolore o disagio nella parte inferiore dell'addome"
            ],
            "symptom_duration_days": 2,
            "temperature_c": 36.7,
            "tests": {
                "leucociti_urinari": True,
                "esterasi_leucocitaria": True,
                "urinocoltura": None
            }
        }
    },


    # ========================================================
    # UTI 2 — FALSE
    # vaginal condition with overlapping urinary symptoms
    # ========================================================

    {
        "case_id": "UTI_002",

        "doctor_note": """
Paziente di 34 anni presenta da 3 giorni bruciore durante
la minzione associato a intenso prurito vaginale,
irritazione vaginale e abbondanti secrezioni vaginali
biancastre.
Riferisce che il fastidio è prevalentemente vulvo-vaginale.
Il quadro viene valutato nel contesto di una sospetta
infezione delle vie urinarie.
""",

        "ehr": {
            "age": 34,
            "sex": "femmina",
            "region": "Liguria",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "amoxicillina",
                    "indication": "faringite"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "bruciore durante la minzione",
                "prurito vaginale",
                "irritazione vaginale",
                "secrezioni vaginali"
            ],
            "symptom_duration_days": 3,
            "temperature_c": 36.6,
            "tests": {
                "leucociti_urinari": False,
                "esterasi_leucocitaria": False,
                "urinocoltura": False
            }
        }
    },


    # ========================================================
    # UTI 3 — TRUE
    # male patient with acute lower urinary symptoms
    # ========================================================

    {
        "case_id": "UTI_003",

        "doctor_note": """
Paziente di 47 anni presenta da 3 giorni disuria,
aumento della frequenza della minzione e urgenza minzionale.
Riferisce dolore sovrapubico e difficoltà a iniziare la
minzione.
Il quadro viene valutato nel contesto di una sospetta
infezione delle vie urinarie inferiori.
""",

        "ehr": {
            "age": 47,
            "sex": "maschio",
            "region": "Lombardia",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "trimetoprim/sulfametossazolo",
                    "indication": "infezione delle vie urinarie"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "disuria",
                "aumento della frequenza della minzione",
                "urgenza minzionale",
                "dolore sovrapubico",
                "difficoltà a iniziare la minzione"
            ],
            "symptom_duration_days": 3,
            "temperature_c": 37.0,
            "tests": {
                "leucociti_urinari": True,
                "esterasi_leucocitaria": True,
                "urinocoltura": True
            }
        }
    },


    # ========================================================
    # UTI 4 — FALSE
    # mild isolated urinary symptom
    # ========================================================

    {
        "case_id": "UTI_004",

        "doctor_note": """
Paziente di 29 anni riferisce da circa 24 ore un lieve
bruciore occasionale durante la minzione.
Non riferisce aumento della frequenza della minzione,
urgenza minzionale o dolore nella parte inferiore
dell'addome.
Il quadro viene valutato nel contesto di una sospetta
infezione delle vie urinarie.
""",

        "ehr": {
            "age": 29,
            "sex": "femmina",
            "region": "Emilia-Romagna",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "azitromicina",
                    "indication": "infezione respiratoria"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "lieve bruciore occasionale durante la minzione"
            ],
            "symptom_duration_hours": 24,
            "temperature_c": 36.5,
            "tests": {
                "leucociti_urinari": False,
                "esterasi_leucocitaria": False,
                "urinocoltura": None
            }
        }
    },


    # ========================================================
    # UTI 5 — EDGE
    # pregnancy
    # ========================================================

    {
        "case_id": "UTI_005",

        "doctor_note": """
Paziente di 31 anni, alla 18ª settimana di gravidanza,
presenta da circa 24 ore disuria acuta, aumento della
frequenza della minzione e urgenza minzionale.
Riferisce lieve dolore e disagio nella parte inferiore
dell'addome.
Il quadro viene valutato nel contesto di una sospetta
infezione delle vie urinarie inferiori.
""",

        "ehr": {
            "age": 31,
            "sex": "femmina",
            "region": "Campania",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "amoxicillina",
                    "indication": "infezione odontogena"
                }
            ],
            "comorbidities": [],
            "pregnancy": True,
            "gestational_age_weeks": 18
        },

        "clinical_data": {
            "symptoms": [
                "disuria acuta",
                "aumento della frequenza della minzione",
                "urgenza minzionale",
                "dolore o disagio nella parte inferiore dell'addome"
            ],
            "symptom_duration_hours": 24,
            "temperature_c": 36.8,
            "tests": {
                "leucociti_urinari": True,
                "esterasi_leucocitaria": True,
                "urinocoltura": None
            }
        }
    },


    # ========================================================
    # CONTROL — UNRELATED
    # ========================================================

    {
        "case_id": "CTRL_001",

        "doctor_note": """
Paziente di 26 anni presenta dolore urente ed eritema
localizzato dopo una puntura di medusa avvenuta circa
2 ore prima.
Riferisce esclusivamente sintomi cutanei locali.
""",

        "ehr": {
            "age": 26,
            "sex": "femmina",
            "region": "Liguria",
            "allergies": [],
            "previous_antibiotics": [
                {
                    "drug": "amoxicillina/acido clavulanico",
                    "indication": "otite media"
                }
            ],
            "comorbidities": [],
            "pregnancy": False
        },

        "clinical_data": {
            "symptoms": [
                "dolore urente locale",
                "eritema localizzato"
            ],
            "symptom_duration_hours": 2,
            "temperature_c": 36.7
        }
    }
]
