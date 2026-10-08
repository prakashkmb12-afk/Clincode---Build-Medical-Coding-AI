import json
import os
from typing import List, Dict, Any

def mine_hard_negatives(
    icd10_codes_path: str = "data/icd10cm/icd10cm_codes.json",
    output_path: str = "data/icd10cm/hard_negatives.json"
) -> List[Dict[str, Any]]:
    """
    FR-10 Hard Negative Mining Pipeline Stage:
    Mines confusable sibling codes (sharing the same category e.g. E11 or I50 but differing in specificity)
    to serve as hard negative training pairs for the cross-encoder reranker.
    """
    if not os.path.exists(icd10_codes_path):
        from clincode_ml.data.prepare_icd10 import export_icd10_dataset
        records = export_icd10_dataset(icd10_codes_path)
    else:
        with open(icd10_codes_path, "r", encoding="utf-8") as f:
            records = json.load(f)

    # Group codes by category
    category_map: Dict[str, List[Dict[str, Any]]] = {}
    for r in records:
        cat = r.get("category", r["code"].split(".")[0])
        category_map.setdefault(cat, []).append(r)

    training_triplets = []
    for cat, items in category_map.items():
        if len(items) > 1:
            for target in items:
                sibling_negatives = [other["code"] for other in items if other["code"] != target["code"]]
                training_triplets.append({
                    "positive_code": target["code"],
                    "description": target["description"],
                    "category": cat,
                    "hard_negatives": sibling_negatives
                })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(training_triplets, f, indent=2)

    print(f"Mined hard negatives for {len(training_triplets)} ICD-10 code targets saved to {output_path}.")
    return training_triplets


if __name__ == "__main__":
    mine_hard_negatives()
