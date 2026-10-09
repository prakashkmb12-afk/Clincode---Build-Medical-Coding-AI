from typing import Dict, Any
from sqlalchemy.orm import Session

from clincode_api.db.models import Document, ChartSubmission, AuditLog, ICD10Code


def generate_fhir_claim_export(db: Session, document_id: str) -> Dict[str, Any]:
    """
    Generates FHIR-flavored Claim resource JSON payload for downstream billing systems.
    Includes patient deid_ref, encounter details, diagnosis coding array, and audit trail.
    """
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise ValueError(f"Document {document_id} not found")

    submission = db.query(ChartSubmission).filter_by(document_id=doc.id).order_by(ChartSubmission.submitted_at.desc()).first()
    final_codes = submission.final_codes if submission else []

    audit_logs = db.query(AuditLog).filter_by(resource_id=str(doc.id)).all()

    diagnoses = []
    for rank, code_str in enumerate(final_codes, start=1):
        code_rec = db.query(ICD10Code).filter_by(code=code_str).first()
        desc = code_rec.description if code_rec else "Diagnosis code"
        diagnoses.append({
            "sequence": rank,
            "diagnosisCodeableConcept": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sid/icd-10-cm",
                        "code": code_str,
                        "display": desc
                    }
                ]
            },
            "type": ["principal"] if rank == 1 else ["secondary"]
        })

    fhir_claim = {
        "resourceType": "Claim",
        "id": f"claim-{doc.id}",
        "status": "active",
        "type": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                    "code": "institutional",
                    "display": "Institutional"
                }
            ]
        },
        "use": "claim",
        "patient": {
            "reference": f"Patient/{doc.external_ref}"
        },
        "created": doc.created_at.isoformat(),
        "item": [],
        "diagnosis": diagnoses,
        "clincode_metadata": {
            "document_id": str(doc.id),
            "external_ref": doc.external_ref,
            "ocr_applied": doc.ocr_applied,
            "version": doc.version,
            "audit_trail": [
                {
                    "timestamp": log.ts.isoformat(),
                    "actor": log.actor,
                    "action": log.action,
                    "detail": log.detail
                } for log in audit_logs
            ]
        }
    }
    return fhir_claim
