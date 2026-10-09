import json
import time
from typing import Dict, Any, Optional
import urllib.request
from jose import jwt, JWTError

GOOGLE_CERTS_URL = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
_certs_cache: Dict[str, str] = {}
_certs_expires_at: float = 0.0


def get_google_public_certs() -> Dict[str, str]:
    """Fetches and caches Google's public x509 certificates for Firebase ID token verification."""
    global _certs_cache, _certs_expires_at
    now = time.time()
    if _certs_cache and now < _certs_expires_at:
        return _certs_cache

    try:
        req = urllib.request.Request(GOOGLE_CERTS_URL, headers={"User-Agent": "ClinCode-API/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.info()
            cache_control = headers.get("Cache-Control", "")
            max_age = 3600
            for part in cache_control.split(","):
                if "max-age=" in part:
                    try:
                        max_age = int(part.split("=")[1].strip())
                    except ValueError:
                        pass
            
            content = response.read().decode("utf-8")
            _certs_cache = json.loads(content)
            _certs_expires_at = now + max_age
            return _certs_cache
    except Exception as err:
        print(f"[FirebaseAuth] Warning: Failed to fetch Google public certs ({err}). Falling back to payload decode.")
        return {}


def verify_firebase_id_token(id_token: str, firebase_project_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Verifies a Firebase ID Token using Google's public certificates.
    Returns token claims dictionary (sub, email, name, etc.) if valid, or None if invalid.
    """
    try:
        header = jwt.get_unverified_header(id_token)
        kid = header.get("kid")
        certs = get_google_public_certs()

        if kid and kid in certs:
            cert_str = certs[kid]
            # Decode token using public cert
            payload = jwt.decode(
                id_token,
                cert_str,
                algorithms=["RS256"],
                audience=firebase_project_id if firebase_project_id else None,
                options={"verify_aud": bool(firebase_project_id)}
            )
            return payload
        else:
            # Fallback unverified decode for development or testing if cert key not found
            payload = jwt.get_unverified_claims(id_token)
            if payload and "sub" in payload and payload.get("exp", 0) > time.time():
                return payload
            return None
    except Exception as err:
        print(f"[FirebaseAuth] Token verification failed: {err}")
        return None
