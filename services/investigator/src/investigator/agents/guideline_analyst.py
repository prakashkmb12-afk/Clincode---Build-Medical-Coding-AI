from investigator.state import ChartInvestigationState, GuidelineFinding
from investigator.tools.guideline_tools import guideline_search


def run_guideline_analyst(state: ChartInvestigationState) -> ChartInvestigationState:
    """
    Guideline Analyst Agent: Performs clause-level GraphRAG over official coding guidelines.
    Returns guideline findings with citations.
    """
    state.tool_call_count += 1
    guideline_findings = []

    for ef in state.evidence_findings:
        topic_matches = guideline_search(ef.entity_text)
        for match in topic_matches:
            guideline_findings.append(GuidelineFinding(
                code_or_topic=ef.entity_text,
                section_num=match["section_num"],
                guideline_text=match["guideline_text"],
                chapter_scope=match["chapter_scope"],
                citation=match["citation"]
            ))

    state.guideline_findings = guideline_findings
    return state
