from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from clincode_api.db.session import get_db
from clincode_api.db.models import User, UserRole
from clincode_api.schemas import LoginRequest, TokenResponse, UserResponse
from clincode_api.auth.jwt import verify_password, create_access_token
from clincode_api.auth.firebase import verify_firebase_id_token
from clincode_api.auth.roles import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class FirebaseLoginRequest(BaseModel):
    id_token: str
    requested_role: Optional[str] = None


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates user credentials and returns JWT token."""
    user = db.query(User).filter_by(username=req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token = create_access_token(data={"sub": str(user.id), "username": user.username, "role": user.role.value})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
        username=user.username,
        role=user.role
    )


@router.post("/firebase-login", response_model=UserResponse)
def firebase_login(req: FirebaseLoginRequest, db: Session = Depends(get_db)):
    """Verifies Firebase ID token, provisions/syncs user profile, and returns authenticated user info."""
    claims = verify_firebase_id_token(req.id_token)
    if not claims or "sub" not in claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token"
        )
    
    email = claims.get("email", f"{claims['sub']}@clincode.ai")
    
    user = db.query(User).filter((User.email == email) | (User.username == email)).first()
    if not user:
        # Determine initial role from request or default to CODER
        target_role = UserRole.CODER
        if req.requested_role and req.requested_role.lower() in [r.value for r in UserRole]:
            target_role = UserRole(req.requested_role.lower())
            
        user = User(
            id=str(uuid.uuid4()),
            username=email,
            email=email,
            password_hash="FIREBASE_OAUTH_USER",
            role=target_role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif req.requested_role:
        # Optional role switcher for demo environment
        if req.requested_role.lower() in [r.value for r in UserRole]:
            user.role = UserRole(req.requested_role.lower())
            db.commit()
            db.refresh(user)

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns details of currently authenticated user."""
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at
    )
