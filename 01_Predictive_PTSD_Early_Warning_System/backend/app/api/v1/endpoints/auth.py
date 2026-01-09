"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from app.core.config import settings
from app.models.user import User, UserRole

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str


class RegisterRequest(BaseModel):
    """Registration request model"""
    email: EmailStr
    username: str
    password: str
    full_name: str
    role: UserRole = UserRole.SOLDIER
    unit_id: int = None
    rank: str = None


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """User login endpoint"""
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.id,
        role=user.role.value
    )


@router.post("/register")
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """User registration endpoint"""
    # Check if user exists
    if db.query(User).filter(User.username == register_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if db.query(User).filter(User.email == register_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(register_data.password)
    new_user = User(
        email=register_data.email,
        username=register_data.username,
        hashed_password=hashed_password,
        full_name=register_data.full_name,
        role=register_data.role,
        unit_id=register_data.unit_id,
        rank=register_data.rank
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user

