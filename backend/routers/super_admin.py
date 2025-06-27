from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.user_service import UserService
from services.tenant_service import TenantService
from services.slot_service import SlotService
from schemas.auth import User, UserAdminResponse, UserCreate
from schemas.tenant import TenantAdminResponse
from schemas.slot import SlotAdminResponse
from utils.auth import get_current_admin_user

router = APIRouter()

# User management endpoints
@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (super admin only)"""
    user_service = UserService(db)
    users = user_service.get_all_users()
    return users

@router.post("/users", response_model=UserAdminResponse)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new user (super admin only)"""
    user_service = UserService(db)
    try:
        user = user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/users/{user_id}/toggle-status")
def toggle_user_status(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Toggle user active status"""
    user_service = UserService(db)
    user = user_service.toggle_user_status(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"}

@router.patch("/users/{user_id}/toggle-admin")
def toggle_admin_status(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Toggle user admin status"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own admin status"
        )
    
    user_service = UserService(db)
    user = user_service.toggle_admin_status(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User {'promoted to admin' if user.is_admin else 'demoted from admin'} successfully"}

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (super admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

# Tenant management endpoints
@router.get("/tenants", response_model=List[TenantAdminResponse])
def get_all_tenants(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all tenants (super admin only)"""
    tenant_service = TenantService(db)
    tenants = tenant_service.get_all_tenants()
    return tenants

@router.patch("/tenants/{tenant_id}/toggle-status")
def toggle_tenant_status(
    tenant_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Toggle tenant active status"""
    tenant_service = TenantService(db)
    tenant = tenant_service.toggle_tenant_status(tenant_id)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return {"message": f"Tenant {'activated' if tenant.is_active else 'deactivated'} successfully"}

# Global slot management
@router.get("/slots", response_model=List[SlotAdminResponse])
def get_all_slots(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all slots from all tenants (super admin only)"""
    slot_service = SlotService(db)
    slots = slot_service.get_all_slots()
    return slots

# Statistics endpoints
@router.get("/stats")
def get_admin_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get platform statistics"""
    user_service = UserService(db)
    tenant_service = TenantService(db)
    slot_service = SlotService(db)
    
    all_users = user_service.get_all_users()
    all_tenants = tenant_service.get_all_tenants()
    all_slots = slot_service.get_all_slots()
    
    active_users = len([u for u in all_users if u.is_active])
    active_tenants = len([t for t in all_tenants if t.is_active])
    booked_slots = len([s for s in all_slots if s.is_booked])
    
    return {
        "total_users": len(all_users),
        "active_users": active_users,
        "admin_users": len([u for u in all_users if u.is_admin]),
        "total_tenants": len(all_tenants),
        "active_tenants": active_tenants,
        "total_slots": len(all_slots),
        "booked_slots": booked_slots,
        "available_slots": len(all_slots) - booked_slots
    }
