import uuid
import random
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from clincode_api.db.models import CodeSuggestion, ReviewAction, ReviewActionEnum, ChartSubmission, Document, DocStatus, User
from clincode_api.audit import log_audit_event


def record_review_action(
    db: Session,
    suggestion_id: str,
    coder: User,
    action: ReviewActionEnum,
    final_code: Optional[str] = None,
    reason: Optional[str] = None
) -> ReviewAction:
    """Records human coder accept / reject / modify action on a code suggestion."""
    suggestion = db.query(CodeSuggestion).filter_by(id=suggestion_id).first()
    if not suggestion:
        raise ValueError(f"Code suggestion {suggestion_id} not found")

    review_action = ReviewAction(
        id=uuid.uuid4(),
        suggestion_id=suggestion.id,
        coder_id=coder.id,
        action=action,
        final_code=final_code or suggestion.icd10_code,
        reason=reason,
        at=datetime.utcnow()
    )
    db.add(review_action)
    db.commit()
    db.refresh(review_action)

    log_audit_event(
        db,
        actor=coder.username,
        action=f"SUGGESTION_{action.value.upper()}",
        resource_type="code_suggestion",
        resource_id=str(suggestion.id),
        detail={"icd10_code": suggestion.icd10_code, "final_code": review_action.final_code, "reason": reason}
    )

    return review_action


def submit_final_chart_coding(
    db: Session,
    document_id: str,
    coder: User,
    final_codes: List[str],
    qa_sample_rate: float = 0.10
) -> ChartSubmission:
    """Finalizes chart coding and triggers double-blind QA routing for 10% of charts."""
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise ValueError(f"Document {document_id} not found")

    qa_pair_id = None
    routed_to_qa = random.random() < qa_sample_rate
    if routed_to_qa:
        qa_pair_id = uuid.uuid4()

    submission = ChartSubmission(
        id=uuid.uuid4(),
        document_id=doc.id,
        coder_id=coder.id,
        final_codes=final_codes,
        qa_pair_id=qa_pair_id,
        submitted_at=datetime.utcnow()
    )
    db.add(submission)

    doc.status = DocStatus.READY
    db.commit()
    db.refresh(submission)

    log_audit_event(
        db,
        actor=coder.username,
        action="CHART_SUBMITTED",
        resource_type="document",
        resource_id=str(doc.id),
        detail={"final_codes": final_codes, "routed_to_qa": routed_to_qa}
    )

    return submission
