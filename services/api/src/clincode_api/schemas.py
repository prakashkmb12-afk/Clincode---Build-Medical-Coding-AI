from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from clincode_api.db.models import DocType, DocStatus, EntityLabel, AssertionStatus, TriageBand, ReviewActionEnum, CdiQueryStatus, UserRole, InvestigationTrigger, InvestigationStatus


# --- Auth Schemas ---
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: UserRole


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime


# --- Document Schemas ---
class DocumentCreate(BaseModel):
    external_ref: str
    doc_type: DocType = DocType.DISCHARGE
    text: str
    is_scanned_pdf: bool = False
    image_bytes_base64: Optional[str] = None


class DocumentResponse(BaseModel):
    document_id: str
    external_ref: str
    doc_type: DocType
    status: DocStatus
    version: int
    ocr_applied: bool
    ocr_low_confidence_count: int
    deid_text: str
    created_at: datetime


class DocumentStatusResponse(BaseModel):
    document_id: str
    status: DocStatus
    stage_progress: List[Dict[str, Any]]
    created_at: datetime


# --- Entity & Evidence Schemas ---
class EntityResponse(BaseModel):
    id: str
    text: str
    label: EntityLabel
    start_char: int
    end_char: int
    section: str
    assertion: AssertionStatus
    concept_id: Optional[str] = None
    ner_conf: float


class EvidenceSpan(BaseModel):
    sentence: str
    start_char: int
    end_char: int
    section: str


# --- Code Suggestion Schemas ---
class CodeSuggestionResponse(BaseModel):
    id: str
    entity_id: str
    icd10_code: str
    description: str
    rank: int
    raw_score: float
    calibrated_conf: float
    band: TriageBand
    justification_md: Optional[str] = None
    grounded: Optional[bool] = None
    evidence_spans: List[EvidenceSpan] = []
    provenance: Optional[Dict[str, Any]] = None


class DocumentSuggestionsResponse(BaseModel):
    document_id: str
    status: DocStatus
    deid_text: str
    entities: List[EntityResponse]
    suggestions: List[CodeSuggestionResponse]


# --- Review Schemas ---
class ReviewActionRequest(BaseModel):
    action: ReviewActionEnum
    final_code: Optional[str] = None
    reason: Optional[str] = None


class ReviewActionResponse(BaseModel):
    action_id: str
    suggestion_id: str
    coder_id: str
    action: ReviewActionEnum
    final_code: Optional[str]
    reason: Optional[str]
    at: datetime


class ChartSubmissionRequest(BaseModel):
    final_codes: List[str]
    notes: Optional[str] = None


class ChartSubmissionResponse(BaseModel):
    submission_id: str
    document_id: str
    coder_id: str
    final_codes: List[str]
    routed_to_qa: bool
    submitted_at: datetime


# --- CDI Query Schemas ---
class CdiQueryResponse(BaseModel):
    id: str
    document_id: str
    gap_type: str
    query_md: str
    status: CdiQueryStatus
    created_at: datetime


# --- Investigation Schemas ---
class InvestigationRequest(BaseModel):
    trigger: Optional[InvestigationTrigger] = InvestigationTrigger.MANUAL


class InvestigationResponse(BaseModel):
    run_id: str
    document_id: str
    trigger: InvestigationTrigger
    status: InvestigationStatus
    started_at: datetime


class InvestigationReportResponse(BaseModel):
    run_id: str
    document_id: str
    status: InvestigationStatus
    trigger: InvestigationTrigger
    report: Optional[Dict[str, Any]] = None
    verifier_pass: Optional[bool] = None
    started_at: datetime
    finished_at: Optional[datetime] = None


# --- Admin & Metrics Schemas ---
class AdminMetricsResponse(BaseModel):
    total_documents: int
    completed_documents: int
    auto_accept_precision: float
    auto_accept_coverage: float
    acceptance_rate_by_band: Dict[str, float]
    acceptance_rate_by_chapter: Dict[str, float]
    grounding_failure_rate: float
    ner_confidence_drift: float


class AdminModelsResponse(BaseModel):
    ner_model_version: str
    assertion_model_version: str
    embedding_model_version: str
    reranker_model_version: str
    prompt_versions: Dict[str, str]
    eval_metrics: Dict[str, float]
