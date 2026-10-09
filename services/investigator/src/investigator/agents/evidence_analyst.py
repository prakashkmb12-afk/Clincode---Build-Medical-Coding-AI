from sqlalchemy.orm import Session
from investigator.state import ChartInvestigationState, EvidenceFinding
from investigator.tools.note_tools import search_note_sections, get_entities


def run_evidence_analyst(state: ChartInvestigationState, db: Session) -> ChartInvestigationState:
    """
    Evidence Analyst Agent: Re-reads the chart around uncertain entities using note tools.
    Surfaces overlooked evidence context as typed EvidenceFindings with exact spans.
    """
    state.tool_call_count += 1
    entities = get_entities(db, state.document_id)

    findings = []
    for ent in entities:
        if ent["assertion"] in ["present", "possible"]:
            snippets = search_note_sections(db, state.document_id, ent["text"])
            snippet_text = snippets[0]["snippet"] if snippets else ent["text"]
            
            findings.append(EvidenceFinding(
                entity_text=ent["text"],
                section=ent["section"],
                evidence_span=snippet_text,
                start_char=ent["start_char"],
                end_char=ent["end_char"],
                relevance_score=0.95
            ))

    state.evidence_findings = findings
    return state
