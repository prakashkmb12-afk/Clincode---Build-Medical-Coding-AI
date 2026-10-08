import pytest
from clincode_pipeline.stages.sectionize import sectionize_note, get_section_for_offset


def test_sectionize_span_preservation_invariant():
    note = (
        "CHIEF COMPLAINT:\nShortness of breath.\n\n"
        "HISTORY OF PRESENT ILLNESS:\nPatient with acute systolic heart failure.\n\n"
        "PAST MEDICAL HISTORY:\nHypertension and type 2 diabetes.\n\n"
        "ASSESSMENT AND PLAN:\nContinue IV diuretics and echocardiogram."
    )

    sections = sectionize_note(note)
    assert len(sections) == 4

    for sec in sections:
        start = sec["start_char"]
        end = sec["end_char"]
        # CRITICAL INVARIANT: note[start:end] MUST equal sec["text"]
        assert note[start:end] == sec["text"]

    # Verify section names
    section_names = [sec["section_name"] for sec in sections]
    assert "CHIEF COMPLAINT" in section_names
    assert "HISTORY OF PRESENT ILLNESS" in section_names
    assert "PAST MEDICAL HISTORY" in section_names
    assert "ASSESSMENT AND PLAN" in section_names

    # Test offset lookups
    hpi_offset = note.find("acute systolic heart failure")
    assert get_section_for_offset(sections, hpi_offset) == "HISTORY OF PRESENT ILLNESS"
