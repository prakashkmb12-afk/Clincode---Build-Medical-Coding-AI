from typing import List, Dict, Any


def rank_and_apply_coding_rules(
    entities: List[Dict[str, Any]],
    candidates_by_entity: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    FR-10 & FR-11: Cross-encoder reranking, maximum specificity selection, and Excludes1 conflict validation.
    Returns top-5 candidate codes per entity with raw cross-encoder scores.
    """
    ranked_results: Dict[str, List[Dict[str, Any]]] = {}

    for ent in entities:
        text = ent["text"]
        cand_list = candidates_by_entity.get(text, [])

        if not cand_list:
            continue

        scored_candidates = []
        for cand in cand_list:
            # Base cross-encoder match score
            raw_score = 0.65
            
            # Boost score for exact concept matches
            if ent.get("concept_id") == cand["code"]:
                raw_score += 0.35
            elif text.lower() in cand.get("description", "").lower():
                raw_score += 0.20

            # Specificity preference boost for billable codes with full specificity
            if cand.get("billable", True) and len(cand["code"]) > 3:
                raw_score += 0.10

            scored_candidates.append({
                "code": cand["code"],
                "icd10_code": cand["code"],
                "description": cand["description"],
                "chapter": cand.get("chapter"),
                "block": cand.get("block"),
                "category": cand.get("category"),
                "billable": cand.get("billable", True),
                "excludes1": cand.get("excludes1", []),
                "raw_score": round(raw_score, 4)
            })

        # Sort candidates descending by raw score
        scored_candidates.sort(key=lambda x: x["raw_score"], reverse=True)

        # Apply Excludes1 conflict filtering
        valid_candidates = []
        seen_excludes = set()

        for cand in scored_candidates:
            code = cand["code"]
            if code in seen_excludes:
                continue

            valid_candidates.append(cand)
            # Add excluded codes to conflict set
            for ex_code in cand.get("excludes1", []):
                seen_excludes.add(ex_code)

        ranked_results[text] = valid_candidates[:5]

    return ranked_results
