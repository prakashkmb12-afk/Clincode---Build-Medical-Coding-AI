import json
import os
from typing import List, Dict, Any

ICD10_SAMPLE_CODES = [
    {
        "code": "I50.23",
        "description": "Acute-on-chronic systolic (congestive) heart failure",
        "chapter": "Diseases of the circulatory system (I00-I99)",
        "block": "Heart failure (I50)",
        "category": "I50",
        "billable": True,
        "excludes1": ["I50.1", "I50.9"],
        "synonyms": ["acute on chronic systolic heart failure", "acute decompensated systolic heart failure"]
    },
    {
        "code": "I50.21",
        "description": "Acute systolic (congestive) heart failure",
        "chapter": "Diseases of the circulatory system (I00-I99)",
        "block": "Heart failure (I50)",
        "category": "I50",
        "billable": True,
        "excludes1": ["I50.22", "I50.23"],
        "synonyms": ["acute systolic heart failure", "acute congestive heart failure"]
    },
    {
        "code": "I50.22",
        "description": "Chronic systolic (congestive) heart failure",
        "chapter": "Diseases of the circulatory system (I00-I99)",
        "block": "Heart failure (I50)",
        "category": "I50",
        "billable": True,
        "excludes1": ["I50.21", "I50.23"],
        "synonyms": ["chronic systolic heart failure"]
    },
    {
        "code": "E11.9",
        "description": "Type 2 diabetes mellitus without complications",
        "chapter": "Endocrine, nutritional and metabolic diseases (E00-E89)",
        "block": "Diabetes mellitus (E08-E13)",
        "category": "E11",
        "billable": True,
        "excludes1": ["E10.9", "E11.21"],
        "synonyms": ["type 2 diabetes", "T2DM"]
    },
    {
        "code": "E11.21",
        "description": "Type 2 diabetes mellitus with diabetic nephropathy",
        "chapter": "Endocrine, nutritional and metabolic diseases (E00-E89)",
        "block": "Diabetes mellitus (E08-E13)",
        "category": "E11",
        "billable": True,
        "excludes1": ["E11.22", "E11.9"],
        "synonyms": ["diabetic nephropathy in type 2 diabetes"]
    },
    {
        "code": "E11.22",
        "description": "Type 2 diabetes mellitus with diabetic chronic kidney disease",
        "chapter": "Endocrine, nutritional and metabolic diseases (E00-E89)",
        "block": "Diabetes mellitus (E08-E13)",
        "category": "E11",
        "billable": True,
        "excludes1": ["E11.21"],
        "synonyms": ["diabetic CKD type 2 diabetes"]
    },
    {
        "code": "I10",
        "description": "Essential (primary) hypertension",
        "chapter": "Diseases of the circulatory system (I00-I99)",
        "block": "Hypertensive diseases (I10-I16)",
        "category": "I10",
        "billable": True,
        "excludes1": ["I11.9", "I12.9"],
        "synonyms": ["hypertension", "high blood pressure", "HTN"]
    },
    {
        "code": "A41.9",
        "description": "Sepsis, unspecified organism",
        "chapter": "Certain infectious and parasitic diseases (A00-B99)",
        "block": "Other septicemia (A40-A41)",
        "category": "A41",
        "billable": True,
        "excludes1": ["R65.20", "R65.21"],
        "synonyms": ["sepsis", "septicemia", "systemic infection"]
    },
    {
        "code": "R65.20",
        "description": "Severe sepsis without septic shock",
        "chapter": "Symptoms, signs and abnormal clinical and laboratory findings (R00-R99)",
        "block": "General symptoms and signs (R68-R69)",
        "category": "R65",
        "billable": True,
        "excludes1": ["A41.9", "R65.21"],
        "synonyms": ["severe sepsis"]
    },
    {
        "code": "I69.30",
        "description": "Unspecified sequelae of cerebral infarction",
        "chapter": "Diseases of the circulatory system (I00-I99)",
        "block": "Cerebrovascular diseases (I60-I69)",
        "category": "I69",
        "billable": True,
        "excludes1": ["I63.9"],
        "synonyms": ["history of stroke", "CVA sequelae"]
    },
    {
        "code": "R07.9",
        "description": "Chest pain, unspecified",
        "chapter": "Symptoms, signs and abnormal clinical and laboratory findings (R00-R99)",
        "block": "Symptoms and signs involving the circulatory and respiratory systems (R00-R09)",
        "category": "R07",
        "billable": True,
        "excludes1": ["I20.9"],
        "synonyms": ["chest pain", "chest tightness"]
    },
    {
        "code": "J18.9",
        "description": "Pneumonia, unspecified organism",
        "chapter": "Diseases of the respiratory system (J00-J99)",
        "block": "Influenza and pneumonia (J09-J18)",
        "category": "J18",
        "billable": True,
        "excludes1": ["J12.9", "J15.9"],
        "synonyms": ["pneumonia", "lung infection"]
    }
]


def export_icd10_dataset(output_path: str = "data/icd10cm/icd10cm_codes.json") -> List[Dict[str, Any]]:
    """Exports structured ICD-10 CM reference dataset to JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ICD10_SAMPLE_CODES, f, indent=2)
    return ICD10_SAMPLE_CODES


if __name__ == "__main__":
    export_icd10_dataset()
    print("Exported ICD-10 reference dataset successfully.")
