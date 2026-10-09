from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import User
from clincode_api.auth.roles import get_current_user
from clincode_api.services.export_service import generate_fhir_claim_export

router = APIRouter(prefix="/documents", tags=["Export"])


@router.get("/{document_id}/export")
def export_fhir_claim(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """FR-19: Exports final approved code set as FHIR-flavored Claim JSON via API."""
    try:
        return generate_fhir_claim_export(db, document_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
