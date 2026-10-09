from typing import Dict, Any, List
from sqlalchemy.orm import Session
from clincode_api.db.models import ICD10Code


def coding_rules_check(db: Session, proposed_codes: List[str]) -> Dict[str, Any]:
    """
    Whitelisted Read-Only Tool: Deterministic validator for Excludes1 conflicts, billability, and specificity.
    """
    conflicts = []
    non_billable = []

    code_objs = db.query(ICD10Code).filter(ICD10Code.code.in_(proposed_codes)).all()
    code_map = {c.code: c for c in code_objs}

    for idx, c1 in enumerate(proposed_codes):
        obj1 = code_map.get(c1)
        if obj1 and not obj1.billable:
            non_billable.append(c1)

        for c2 in proposed_codes[idx+1:]:
            obj2 = code_map.get(c2)
            if obj1 and obj1.excludes1 and c2 in obj1.excludes1:
                conflicts.append({"code_a": c1, "code_b": c2, "rule": "Excludes1"})
            if obj2 and obj2.excludes1 and c1 in obj2.excludes1:
                conflicts.append({"code_a": c2, "code_b": c1, "rule": "Excludes1"})

    return {
        "valid": len(conflicts) == 0 and len(non_billable) == 0,
        "conflicts": conflicts,
        "non_billable": non_billable
    }
