from clincode_pipeline.stages.ner import run_clinical_ner
from clincode_pipeline.stages.sectionize import sectionize_note


def test_clinical_ner_extraction_and_spans():
    text = "CHIEF COMPLAINT:\nShortness of breath and worsening lower extremity swelling."
    sections = sectionize_note(text)
    entities = run_clinical_ner(text, sections)

    assert len(entities) > 0
    for ent in entities:
        start = ent["start_char"]
        end = ent["end_char"]
        # Span preservation invariant check
        assert text[start:end] == ent["text"]
        assert ent["label"] in ["condition", "procedure", "medication", "anatomy"]
