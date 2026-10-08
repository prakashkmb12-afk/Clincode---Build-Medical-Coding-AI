import random
from typing import List, Dict, Any

NEGATION_TEMPLATES = [
    "Patient denies {entity}.",
    "No evidence of {entity} on evaluation.",
    "Patient is negative for {entity}.",
    "Without signs or symptoms of {entity}."
]

FAMILY_TEMPLATES = [
    "Family history of {entity}.",
    "Father had {entity}.",
    "Mother with history of {entity}."
]


def augment_assertion_dataset(samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    FR-6 & §14 Data Augmentation Stage:
    Augments training samples with clinical negation and family history templates
    to ensure zero-tolerance for negated conditions in auto-accept band.
    """
    augmented = list(samples)

    for sample in samples:
        entity = sample.get("entity_text", "condition")

        # Generate synthetic negated example
        neg_text = random.choice(NEGATION_TEMPLATES).format(entity=entity)
        augmented.append({
            "text": neg_text,
            "entity_text": entity,
            "assertion": "absent"
        })

        # Generate synthetic family history example
        fam_text = random.choice(FAMILY_TEMPLATES).format(entity=entity)
        augmented.append({
            "text": fam_text,
            "entity_text": entity,
            "assertion": "family"
        })

    return augmented
