from investigator.state import ChartInvestigationState


def run_query_drafter(state: ChartInvestigationState) -> ChartInvestigationState:
    """
    Query Drafter Agent: Drafts compliant, non-leading physician CDI queries when documentation gaps exist.
    """
    state.tool_call_count += 1
    cdi_queries = []

    for ef in state.evidence_findings:
        if "sepsis" in ef.entity_text.lower() or "possible" in ef.entity_text.lower():
            cdi_queries.append({
                "gap_type": "missing_acuity_and_organ_dysfunction",
                "query_md": (
                    "**Physician Documentation Clarification Query**\n\n"
                    f"**Documented Finding:** '{ef.evidence_span}'.\n"
                    "**Clarification Requested:** Please document if the patient met criteria for acute organ dysfunction / severe sepsis, or if sepsis was ruled out."
                )
            })

    state.cdi_queries = cdi_queries
    return state
