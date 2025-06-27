from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import UserCreate
from utils.auth import get_password_hash, verify_password
from config.settings import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate, is_admin: bool = False) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_admin_user_if_not_exists(self):
        """Create admin user if it doesn't exist"""
        admin_user = self.get_user_by_email(settings.ADMIN_EMAIL)
        if not admin_user:
            admin_data = UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD
            )
            self.create_user(admin_data, is_admin=True)
