from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.tenant_service import TenantService
from services.slot_service import SlotService
from schemas.tenant import TenantCreate, TenantUpdate, TenantResponse, TenantPublic
from schemas.slot import SlotPublicResponse, SlotBook, BookingConfirmation
from schemas.auth import User
from utils.auth import get_current_user, get_current_admin_user

router = APIRouter()

# Public endpoints for tenant booking pages
@router.get("/{username}", response_model=TenantPublic)
def get_tenant_public(username: str, db: Session = Depends(get_db)):
    """Get public tenant information"""
    tenant_service = TenantService(db)
    tenant = tenant_service.get_tenant_by_username(username)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return tenant

@router.get("/{username}/slots", response_model=List[SlotPublicResponse])
def get_tenant_available_slots(username: str, db: Session = Depends(get_db)):
    """Get available slots for a tenant"""
    slot_service = SlotService(db)
    slots = slot_service.get_available_slots_for_tenant(username)
    return slots

@router.post("/{username}/slots/{slot_id}/book", response_model=BookingConfirmation)
async def book_tenant_slot(
    username: str,
    slot_id: int,
    booking_data: SlotBook,
    db: Session = Depends(get_db)
):
    """Book a slot for a specific tenant"""
    slot_service = SlotService(db)
    
    booked_slot = await slot_service.book_slot(slot_id, booking_data, username)
    
    return BookingConfirmation(
        message="Slot successfully booked",
        slot_id=booked_slot.id,
        datetime=booked_slot.datetime,
        tenant_username=username
    )

# User dashboard endpoints
@router.get("/", response_model=List[TenantResponse])
def get_user_tenants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tenants owned by the current user"""
    tenant_service = TenantService(db)
    tenants = tenant_service.get_user_tenants(current_user.id)
    return tenants

@router.post("/", response_model=TenantResponse)
def create_tenant(
    tenant_data: TenantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tenant"""
    tenant_service = TenantService(db)
    tenant = tenant_service.create_tenant(tenant_data, current_user.id)
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a tenant"""
    tenant_service = TenantService(db)
    tenant = tenant_service.update_tenant(tenant_id, tenant_data, current_user.id)
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return tenant

@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a tenant"""
    tenant_service = TenantService(db)
    success = tenant_service.delete_tenant(tenant_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return {"message": "Tenant deleted successfully"}
