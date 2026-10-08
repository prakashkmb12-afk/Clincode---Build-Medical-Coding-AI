import re
import json
from typing import Dict, Tuple, List, Any
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY", "3X-sX-s3Z4Z_X_s3Z4Z_X_s3Z4Z_X_s3Z4Z_X_s3Z4Z=")

def get_fernet_cipher() -> Fernet:
    """Returns a valid Fernet cipher instance from key."""
    key = FERNET_KEY
    if len(key) != 44:
        # Generate a deterministic 32-byte urlsafe base64 key
        import base64, hashlib
        key = base64.urlsafe_b64encode(hashlib.sha256(FERNET_KEY.encode()).digest()).decode()
    return Fernet(key.encode())


# Regex patterns for PHI detection
PHI_PATTERNS = [
    ("SSN", r"\b\d{3}-\d{2}-\d{4}\b"),
    ("MRN", r"\bMRN[:\s]*#?\s*(\d{6,10})\b"),
    ("PHONE", r"\b(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b"),
    ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("DATE", r"\b(0?[1-9]|1[0-2])[\/.-](0?[1-9]|[12]\d|3[01])[\/.-](19|20)?\d{2}\b"),
    ("ZIP", r"\b\d{5}(?:-\d{4})?\b"),
]

# Common doctor/patient name patterns
NAME_PATTERNS = [
    r"\bDr\.\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
    r"\bPatient:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
    r"\bJohn\s+Doe\b",
    r"\bJane\s+Doe\b"
]


def deidentify_text(raw_text: str) -> Tuple[str, bytes, bytes, Dict[str, Any]]:
    """
    De-identifies free-text clinical notes.
    Replaces detected PHI with typed placeholders.
    Returns:
      (deid_text, raw_text_encrypted, phi_map_encrypted, phi_summary)
    """
    cipher = get_fernet_cipher()

    # Encrypt raw text
    raw_text_encrypted = cipher.encrypt(raw_text.encode("utf-8"))

    deid_text = raw_text
    phi_map = {}
    counters = {}

    # Match Regex PHI patterns
    for tag, pattern in PHI_PATTERNS:
        for match in re.finditer(pattern, raw_text):
            phi_val = match.group(0)
            if phi_val not in phi_map:
                count = counters.get(tag, 0) + 1
                counters[tag] = count
                placeholder = f"[{tag}_{count}]"
                phi_map[phi_val] = placeholder

    # Match Name patterns
    for pattern in NAME_PATTERNS:
        for match in re.finditer(pattern, raw_text):
            phi_val = match.group(0)
            if phi_val not in phi_map:
                count = counters.get("NAME", 0) + 1
                counters["NAME"] = count
                placeholder = f"[NAME_{count}]"
                phi_map[phi_val] = placeholder

    # Replace PHI strings in text
    for phi_val, placeholder in phi_map.items():
        deid_text = deid_text.replace(phi_val, placeholder)

    # Encrypt PHI map
    phi_map_json = json.dumps(phi_map)
    phi_map_encrypted = cipher.encrypt(phi_map_json.encode("utf-8"))

    phi_summary = {
        "total_phi_scrubbed": len(phi_map),
        "placeholders": list(phi_map.values())
    }

    return deid_text, raw_text_encrypted, phi_map_encrypted, phi_summary


def reidentify_text(deid_text: str, phi_map_encrypted: bytes) -> str:
    """
    Re-identifies de-identified text using the encrypted PHI map.
    Only authorized for administrative/audit workflows.
    """
    cipher = get_fernet_cipher()
    phi_map_json = cipher.decrypt(phi_map_encrypted).decode("utf-8")
    phi_map = json.loads(phi_map_json)

    reconstructed_text = deid_text
    # Reverse replacement: placeholder -> original value
    for phi_val, placeholder in phi_map.items():
        reconstructed_text = reconstructed_text.replace(placeholder, phi_val)

    return reconstructed_text
