from typing import List, Dict, Any

BIO_TAG_SCHEME = [
    "O",
    "B-CONDITION", "I-CONDITION",
    "B-PROCEDURE", "I-PROCEDURE",
    "B-MEDICATION", "I-MEDICATION",
    "B-ANATOMY", "I-ANATOMY"
]


def convert_spans_to_bio_tags(text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts entity character spans into tokenized BIO-tagged sequences
    for Bio_ClinicalBERT token classification training.
    """
    tokens = text.split()
    token_tags = ["O"] * len(tokens)

    # Simple word boundary mapping
    current_char = 0
    token_spans = []
    for token in tokens:
        start = text.find(token, current_char)
        end = start + len(token)
        token_spans.append((start, end))
        current_char = end

    for ent in entities:
        ent_start, ent_end = ent["start_char"], ent["end_char"]
        label = ent["label"].upper()

        is_first = True
        for i, (t_start, t_end) in enumerate(token_spans):
            if t_start >= ent_start and t_end <= ent_end:
                tag = f"B-{label}" if is_first else f"I-{label}"
                token_tags[i] = tag
                is_first = False

    return [{"token": t, "tag": tag} for t, tag in zip(tokens, token_tags)]
