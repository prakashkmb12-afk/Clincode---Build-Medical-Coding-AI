from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EvidenceFinding(BaseModel):
    entity_text: str
    section: str
    evidence_span: str
    start_char: int
    end_char: int
    relevance_score: float = 1.0


class GuidelineFinding(BaseModel):
    code_or_topic: str
    section_num: str
    guideline_text: str
    chapter_scope: str
    citation: str


class HierarchyFinding(BaseModel):
    code: str
    parent_code: Optional[str] = None
    specific_siblings: List[str] = []
    excludes1_partners: List[str] = []
    has_excludes1_conflict: bool = False
    conflict_code: Optional[str] = None


class PrecedentFinding(BaseModel):
    similar_chart_ref: str
    similarity_score: float
    approved_codes: List[str]
    outcome_summary: str


class InvestigationRecommendation(BaseModel):
    icd10_code: str
    description: str
    rank: int
    confidence: float
    evidence_span: str
    guideline_citation: str
    precedent_ref: Optional[str] = None
    verifier_passed: bool = True
    dissent_note: Optional[str] = None


class ChartInvestigationState(BaseModel):
    document_id: str
    trigger: str
    status: str = "queued"
    tool_call_count: int = 0
    revision_loop_count: int = 0
    max_tool_calls: int = 12
    max_revision_loops: int = 2

    # Agent Findings
    evidence_findings: List[EvidenceFinding] = []
    guideline_findings: List[GuidelineFinding] = []
    hierarchy_findings: List[HierarchyFinding] = []
    precedent_findings: List[PrecedentFinding] = []

    # Final outputs
    recommendations: List[InvestigationRecommendation] = []
    cdi_queries: List[Dict[str, Any]] = []
    dissenting_notes: List[str] = []
    verifier_pass: Optional[bool] = None
