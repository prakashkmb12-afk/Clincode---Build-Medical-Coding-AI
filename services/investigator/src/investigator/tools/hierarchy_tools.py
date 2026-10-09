from typing import Dict, Any, List
from sqlalchemy.orm import Session
from clincode_api.db.models import ICD10Code


def icd10_hierarchy(db: Session, code: str) -> Dict[str, Any]:
    """
    Whitelisted Read-Only Tool: Navigates the ICD-10 tree.
    Returns parent category code, specific sibling codes, billable status, and Excludes1 partners.
    """
    record = db.query(ICD10Code).filter_by(code=code).first()
    if not record:
        return {
            "code": code,
            "found": False,
            "parent_code": code[:3] if len(code) > 3 else None,
            "siblings": [],
            "excludes1": []
        }

    category = record.category or code[:3]
    siblings = db.query(ICD10Code).filter(ICD10Code.category == category, ICD10Code.code != code).all()

    return {
        "code": record.code,
        "found": True,
        "description": record.description,
        "chapter": record.chapter,
        "block": record.block,
        "category": record.category,
        "billable": record.billable,
        "parent_code": category,
        "siblings": [s.code for s in siblings],
        "excludes1": record.excludes1 or []
    }
