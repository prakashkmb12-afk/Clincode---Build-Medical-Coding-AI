from typing import List, Dict, Any
from sqlalchemy.orm import Session
from clincode_api.db.models import Document, Entity, DocStatus


def search_note_sections(db: Session, document_id: str, query: str) -> List[Dict[str, Any]]:
    """
    Whitelisted Read-Only Tool: Searches clinical note text sections for keyword occurrences.
    Returns matching text snippets with section names and character offsets.
    """
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        return []

    results = []
    text_lower = doc.deid_text.lower()
    query_lower = query.lower()

    pos = 0
    while True:
        idx = text_lower.find(query_lower, pos)
        if idx == -1:
            break
        
        snippet_start = max(0, idx - 40)
        snippet_end = min(len(doc.deid_text), idx + len(query) + 40)
        snippet = doc.deid_text[snippet_start:snippet_end]

        results.append({
            "query": query,
            "snippet": snippet,
            "start_char": idx,
            "end_char": idx + len(query)
        })
        pos = idx + len(query)

    return results


def get_entities(db: Session, document_id: str) -> List[Dict[str, Any]]:
    """
    Whitelisted Read-Only Tool: Retrieves extracted entities and assertion states for a chart.
    """
    entities = db.query(Entity).filter_by(document_id=document_id).all()
    return [
        {
            "id": str(e.id),
            "text": e.text,
            "label": e.label.value,
            "section": e.section,
            "assertion": e.assertion.value,
            "start_char": e.start_char,
            "end_char": e.end_char
        } for e in entities
    ]
