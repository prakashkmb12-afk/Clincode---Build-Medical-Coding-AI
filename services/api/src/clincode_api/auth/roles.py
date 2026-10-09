from typing import List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid

from clincode_api.db.session import get_db
from clincode_api.db.models import User, UserRole
from clincode_api.auth.jwt import decode_access_token
from clincode_api.auth.firebase import verify_firebase_id_token

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency for resolving current authenticated user from Firebase or local JWT token."""
    if not credentials:
        # Fallback for dev / unauthenticated requests (demo fallback user)
        demo_user = db.query(User).filter_by(username="demo_coder").first()
        if demo_user:
            return demo_user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required"
        )
    
    token = credentials.credentials
    
    # 1. Try local JWT token decode
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        user_id = payload["sub"]
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            return user

    # 2. Try Firebase ID Token decode
    firebase_claims = verify_firebase_id_token(token)
    if firebase_claims and "sub" in firebase_claims:
        fb_uid = firebase_claims["sub"]
        email = firebase_claims.get("email", f"{fb_uid}@clincode.ai")
        name = firebase_claims.get("name", email.split("@")[0])

        # Find existing user by email or firebase UID
        user = db.query(User).filter((User.email == email) | (User.username == email)).first()
        if not user:
            # Auto-provision user with default CODER role
            user = User(
                id=str(uuid.uuid4()),
                username=email,
                email=email,
                password_hash="FIREBASE_OAUTH_USER",
                role=UserRole.CODER
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token"
    )


def require_roles(allowed_roles: List[UserRole]) -> Callable:
    """Dependency factory for enforcing Role-Based Access Control (RBAC)."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action requires one of the following roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker
