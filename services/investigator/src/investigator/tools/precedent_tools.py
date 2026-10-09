from typing import List, Dict, Any
from investigator.memory.precedents import search_precedent_memory


def similar_charts(query_text: str) -> List[Dict[str, Any]]:
    """
    Whitelisted Read-Only Tool: Retrieves top-k similar approved past chart codings.
    """
    return search_precedent_memory(query_text)
