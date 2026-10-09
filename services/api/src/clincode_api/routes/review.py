from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import User, UserRole
from clincode_api.schemas import ReviewActionRequest, ReviewActionResponse, ChartSubmissionRequest, ChartSubmissionResponse
from clincode_api.auth.roles import get_current_user, require_roles
from clincode_api.services.review_service import record_review_action, submit_final_chart_coding

router = APIRouter(prefix="", tags=["Review Console"])


@router.post("/suggestions/{suggestion_id}/action", response_model=ReviewActionResponse)
def review_action(
    suggestion_id: str,
    req: ReviewActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.CODER, UserRole.MANAGER]))
):
    """
    FR-16 & FR-17: Records coder action (accept/reject/modify) on a suggested code.
    Captures reasoning and feeds labeled feedback dataset.
    """
    try:
        action_rec = record_review_action(
            db,
            suggestion_id=suggestion_id,
            coder=current_user,
            action=req.action,
            final_code=req.final_code,
            reason=req.reason
        )
        return ReviewActionResponse(
            action_id=str(action_rec.id),
            suggestion_id=str(action_rec.suggestion_id),
            coder_id=str(action_rec.coder_id),
            action=action_rec.action,
            final_code=action_rec.final_code,
            reason=action_rec.reason,
            at=action_rec.at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/documents/{document_id}/submit", response_model=ChartSubmissionResponse)
def submit_chart(
    document_id: str,
    req: ChartSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.CODER, UserRole.MANAGER]))
):
    """
    Finalizes chart review and submits approved code set.
    Optionally routes a fraction of charts to double-blind QA mode.
    """
    try:
        submission = submit_final_chart_coding(
            db,
            document_id=document_id,
            coder=current_user,
            final_codes=req.final_codes
        )
        return ChartSubmissionResponse(
            submission_id=str(submission.id),
            document_id=str(submission.document_id),
            coder_id=str(submission.coder_id),
            final_codes=submission.final_codes,
            routed_to_qa=submission.qa_pair_id is not None,
            submitted_at=submission.submitted_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
