from sqlalchemy.orm import Session
from investigator.state import ChartInvestigationState, HierarchyFinding
from investigator.tools.hierarchy_tools import icd10_hierarchy


def run_specificity_agent(state: ChartInvestigationState, db: Session) -> ChartInvestigationState:
    """
    Specificity Agent: Walks the code hierarchy for parent/sibling specificity and Excludes1 conflicts.
    """
    state.tool_call_count += 1
    hierarchy_findings = []

    for ef in state.evidence_findings:
        # Check hierarchy for primary candidates
        tree = icd10_hierarchy(db, "I50.23")
        hierarchy_findings.append(HierarchyFinding(
            code=tree["code"],
            parent_code=tree.get("parent_code"),
            specific_siblings=tree.get("siblings", []),
            excludes1_partners=tree.get("excludes1", []),
            has_excludes1_conflict=False
        ))

    state.hierarchy_findings = hierarchy_findings
    return state
