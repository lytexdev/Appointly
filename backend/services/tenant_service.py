from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.tenants import Tenant
from models.user import User
from schemas.tenant import TenantCreate, TenantUpdate
from fastapi import HTTPException, status

class TenantService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_tenant_by_username(self, username: str) -> Optional[Tenant]:
        """Get tenant by username"""
        return self.db.query(Tenant).filter(
            and_(
                Tenant.username == username.lower(),
                Tenant.is_active == True
            )
        ).first()
    
    def get_tenant_by_id(self, tenant_id: int) -> Optional[Tenant]:
        """Get tenant by ID"""
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    def get_all_tenants(self) -> List[Tenant]:
        """Get all tenants (admin view)"""
        return self.db.query(Tenant).order_by(Tenant.created_at.desc()).all()
    
    def get_user_tenants(self, user_id: int) -> List[Tenant]:
        """Get all tenants owned by a user"""
        return self.db.query(Tenant).filter(Tenant.owner_id == user_id).all()
    
    def create_tenant(self, tenant_data: TenantCreate, owner_id: int) -> Tenant:
        """Create a new tenant"""
        # Check if username is already taken
        existing = self.db.query(Tenant).filter(
            Tenant.username == tenant_data.username.lower()
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )
        
        tenant = Tenant(
            username=tenant_data.username.lower(),
            display_name=tenant_data.display_name,
            email=tenant_data.email,
            title=tenant_data.title,
            description=tenant_data.description,
            primary_color=tenant_data.primary_color,
            logo_url=tenant_data.logo_url,
            business_name=tenant_data.business_name,
            business_address=tenant_data.business_address,
            business_phone=tenant_data.business_phone,
            business_email=tenant_data.business_email,
            allow_public_booking=tenant_data.allow_public_booking,
            booking_lead_time_hours=tenant_data.booking_lead_time_hours,
            max_advance_days=tenant_data.max_advance_days,
            owner_id=owner_id
        )
        
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def update_tenant(self, tenant_id: int, tenant_data: TenantUpdate, user_id: int) -> Optional[Tenant]:
        """Update tenant (only by owner or admin)"""
        tenant = self.get_tenant_by_id(tenant_id)
        
        if not tenant:
            return None
        
        # Check ownership (unless user is admin)
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user.is_admin and tenant.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this tenant"
            )
        
        # Update fields
        update_data = tenant_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)
        
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def delete_tenant(self, tenant_id: int, user_id: int) -> bool:
        """Delete tenant (only by owner or admin)"""
        tenant = self.get_tenant_by_id(tenant_id)
        
        if not tenant:
            return False
        
        # Check ownership (unless user is admin)
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user.is_admin and tenant.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this tenant"
            )
        
        self.db.delete(tenant)
        self.db.commit()
        return True
    
    def toggle_tenant_status(self, tenant_id: int) -> Optional[Tenant]:
        """Toggle tenant active status (admin only)"""
        tenant = self.get_tenant_by_id(tenant_id)
        if tenant:
            tenant.is_active = not tenant.is_active
            self.db.commit()
            self.db.refresh(tenant)
        return tenant