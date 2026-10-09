from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import CdiQuery, User, UserRole
from clincode_api.schemas import CdiQueryResponse
from clincode_api.auth.roles import get_current_user, require_roles

router = APIRouter(prefix="/documents", tags=["CDI Queries"])


@router.get("/{document_id}/queries", response_model=List[CdiQueryResponse])
def get_cdi_queries(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """FR-14: Returns documentation-gap physician CDI queries for a chart."""
    queries = db.query(CdiQuery).filter_by(document_id=document_id).all()
    return [
        CdiQueryResponse(
            id=str(q.id),
            document_id=str(q.document_id),
            gap_type=q.gap_type,
            query_md=q.query_md,
            status=q.status,
            created_at=q.created_at
        ) for q in queries
    ]
