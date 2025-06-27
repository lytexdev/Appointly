from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import get_db
from config.settings import settings
from services.auth_service import AuthService
from schemas.auth import Token, UserLogin, User, UserCreate
from utils.auth import create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=User)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    auth_service = AuthService(db)
    
    try:
        user = auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    auth_service = AuthService(db)
    
    # Create admin user if it doesn't exist
    auth_service.create_admin_user_if_not_exists()
    
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    from services.user_service import UserService
    user_service = UserService(db)
    user_service.update_last_login(user.id)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=Token)
def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login with JSON payload and get access token"""
    auth_service = AuthService(db)
    
    # Create admin user if it doesn't exist
    auth_service.create_admin_user_if_not_exists()
    
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Update last login
    from services.user_service import UserService
    user_service = UserService(db)
    user_service.update_last_login(user.id)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print(f"Created token for user: {user.email}")  # Debug print
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    print(f"Retrieved user: {current_user.email}")  # Debug print
    return current_user

@router.get("/test-token")
def test_token(current_user: User = Depends(get_current_user)):
    """Test endpoint to debug token issues"""
    return {"message": "Token is valid", "user_email": current_user.email}
