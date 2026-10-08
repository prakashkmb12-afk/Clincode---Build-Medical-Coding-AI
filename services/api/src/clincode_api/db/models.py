import enum
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, SmallInteger, BigInteger,
    DateTime, ForeignKey, Enum as SQLEnum, LargeBinary, JSON, TypeDecorator
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import relationship

from clincode_api.db.session import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses String(36).
    """
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(str(value)))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(str(value))
            else:
                return value


# Dialect-compatible JSON type
JSONType = JSONB().with_variant(JSON(), "sqlite")


class DocType(str, enum.Enum):
    DISCHARGE = "discharge"
    RADIOLOGY = "radiology"
    PROGRESS = "progress"


class DocStatus(str, enum.Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    QUARANTINED = "quarantined"


class EntityLabel(str, enum.Enum):
    CONDITION = "condition"
    PROCEDURE = "procedure"
    MEDICATION = "medication"
    ANATOMY = "anatomy"


class AssertionStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    POSSIBLE = "possible"
    CONDITIONAL = "conditional"
    HISTORICAL = "historical"
    FAMILY = "family"


class TriageBand(str, enum.Enum):
    AUTO = "auto"
    REVIEW = "review"
    LOW = "low"


class ReviewActionEnum(str, enum.Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    MODIFY = "modify"


class CdiQueryStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ANSWERED = "answered"
    DISMISSED = "dismissed"


class UserRole(str, enum.Enum):
    CODER = "coder"
    CDI_SPECIALIST = "cdi_specialist"
    MANAGER = "manager"
    ADMIN = "admin"


class InvestigationTrigger(str, enum.Enum):
    LOW_CONFIDENCE = "low_confidence"
    ASSERTION_CONFLICT = "assertion_conflict"
    EXCLUDES1 = "excludes1"
    MANUAL = "manual"


class InvestigationStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    READY = "ready"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CODER)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    review_actions = relationship("ReviewAction", back_populates="coder")
    chart_submissions = relationship("ChartSubmission", back_populates="coder")


class Document(Base):
    __tablename__ = "documents"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    external_ref = Column(String(64), nullable=False, index=True)
    doc_type = Column(SQLEnum(DocType), nullable=False, default=DocType.DISCHARGE)
    raw_text_encrypted = Column(LargeBinary, nullable=True)
    deid_text = Column(Text, nullable=False)
    phi_map_encrypted = Column(LargeBinary, nullable=True)
    status = Column(SQLEnum(DocStatus), nullable=False, default=DocStatus.RECEIVED, index=True)
    version = Column(Integer, nullable=False, default=1)
    ocr_applied = Column(Boolean, nullable=False, default=False)
    ocr_low_confidence_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    pipeline_runs = relationship("PipelineRun", back_populates="document", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="document", cascade="all, delete-orphan")
    code_suggestions = relationship("CodeSuggestion", back_populates="document", cascade="all, delete-orphan")
    chart_submissions = relationship("ChartSubmission", back_populates="document", cascade="all, delete-orphan")
    cdi_queries = relationship("CdiQuery", back_populates="document", cascade="all, delete-orphan")
    investigation_runs = relationship("InvestigationRun", back_populates="document", cascade="all, delete-orphan")


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    stage = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    model_versions = Column(JSONType, nullable=True)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    error = Column(Text, nullable=True)

    document = relationship("Document", back_populates="pipeline_runs")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    label = Column(SQLEnum(EntityLabel), nullable=False)
    start_char = Column(Integer, nullable=False)
    end_char = Column(Integer, nullable=False)
    section = Column(String(64), nullable=False, default="UNKNOWN")
    assertion = Column(SQLEnum(AssertionStatus), nullable=False, default=AssertionStatus.PRESENT)
    concept_id = Column(String(32), nullable=True)
    ner_conf = Column(Float, nullable=False, default=1.0)

    document = relationship("Document", back_populates="entities")
    suggestions = relationship("CodeSuggestion", back_populates="entity", cascade="all, delete-orphan")


class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    code = Column(String(16), primary_key=True)
    description = Column(Text, nullable=False)
    chapter = Column(String(128), nullable=True)
    block = Column(String(128), nullable=True)
    category = Column(String(64), nullable=True)
    billable = Column(Boolean, nullable=False, default=True)
    excludes1 = Column(JSONType, nullable=True)
    synonyms = Column(JSONType, nullable=True)

    suggestions = relationship("CodeSuggestion", back_populates="icd10_record")


class CodeSuggestion(Base):
    __tablename__ = "code_suggestions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(GUID(), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    icd10_code = Column(String(16), ForeignKey("icd10_codes.code"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    rank = Column(SmallInteger, nullable=False)
    raw_score = Column(Float, nullable=False)
    calibrated_conf = Column(Float, nullable=False)
    band = Column(SQLEnum(TriageBand), nullable=False, index=True)
    justification_md = Column(Text, nullable=True)
    grounded = Column(Boolean, nullable=True)
    evidence_spans = Column(JSONType, nullable=True)
    provenance = Column(JSONType, nullable=True)

    document = relationship("Document", back_populates="code_suggestions")
    entity = relationship("Entity", back_populates="suggestions")
    icd10_record = relationship("ICD10Code", back_populates="suggestions")
    review_actions = relationship("ReviewAction", back_populates="suggestion", cascade="all, delete-orphan")


class ReviewAction(Base):
    __tablename__ = "review_actions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    suggestion_id = Column(GUID(), ForeignKey("code_suggestions.id", ondelete="CASCADE"), nullable=False)
    coder_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    action = Column(SQLEnum(ReviewActionEnum), nullable=False)
    final_code = Column(String(16), nullable=True)
    reason = Column(String(128), nullable=True)
    at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    suggestion = relationship("CodeSuggestion", back_populates="review_actions")
    coder = relationship("User", back_populates="review_actions")


class ChartSubmission(Base):
    __tablename__ = "chart_submissions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    coder_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    final_codes = Column(JSONType, nullable=False)
    qa_pair_id = Column(GUID(), nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="chart_submissions")
    coder = relationship("User", back_populates="chart_submissions")


class CdiQuery(Base):
    __tablename__ = "cdi_queries"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    gap_type = Column(String(64), nullable=False)
    query_md = Column(Text, nullable=False)
    status = Column(SQLEnum(CdiQueryStatus), nullable=False, default=CdiQueryStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="cdi_queries")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    actor = Column(String(128), nullable=False)
    action = Column(String(64), nullable=False)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(128), nullable=False)
    detail = Column(JSONType, nullable=False, default=dict)


class InvestigationRun(Base):
    __tablename__ = "investigation_runs"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID(), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    trigger = Column(SQLEnum(InvestigationTrigger), nullable=False)
    status = Column(SQLEnum(InvestigationStatus), nullable=False, default=InvestigationStatus.QUEUED)
    report = Column(JSONType, nullable=True)
    agent_versions = Column(JSONType, nullable=True)
    verifier_pass = Column(Boolean, nullable=True)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    document = relationship("Document", back_populates="investigation_runs")
