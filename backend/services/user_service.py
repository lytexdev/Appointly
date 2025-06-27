from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import UserCreate, UserUpdate
from utils.auth import get_password_hash
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """Get all users (admin only)"""
        return self.db.query(User).order_by(User.created_at.desc()).all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate, is_admin: bool = False) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        
        # Hash password if provided
        if 'password' in update_data:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
        
        # Check email uniqueness if changed
        if 'email' in update_data and update_data['email'] != user.email:
            existing_user = self.get_user_by_email(update_data['email'])
            if existing_user:
                raise ValueError("Email already registered")
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def toggle_user_status(self, user_id: int) -> Optional[User]:
        """Toggle user active status"""
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = not user.is_active
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def toggle_admin_status(self, user_id: int) -> Optional[User]:
        """Toggle user admin status"""
        user = self.get_user_by_id(user_id)
        if user:
            user.is_admin = not user.is_admin
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.now()
            self.db.commit()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user (admin only, careful with cascading!)"""
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
