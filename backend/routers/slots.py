from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.slot_service import SlotService
from schemas.slot import SlotResponse, SlotCreate, SlotAdminResponse
from schemas.auth import User
from utils.auth import get_current_user

router = APIRouter()

# Tenant slot management endpoints
@router.get("/tenants/{tenant_id}/slots", response_model=List[SlotAdminResponse])
def get_tenant_slots(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all slots for a specific tenant (owner view)"""
    slot_service = SlotService(db)
    slots = slot_service.get_tenant_slots(tenant_id)
    return slots

@router.post("/tenants/{tenant_id}/slots", response_model=SlotResponse)
def create_slot_for_tenant(
    tenant_id: int,
    slot_data: SlotCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new slot for a tenant"""
    # Override tenant_id from URL
    slot_data.tenant_id = tenant_id
    
    slot_service = SlotService(db)
    slot = slot_service.create_slot(slot_data, current_user.id)
    return slot

@router.delete("/slots/{slot_id}")
def delete_slot(
    slot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a slot"""
    slot_service = SlotService(db)
    success = slot_service.delete_slot(slot_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot not found"
        )
    
    return {"message": "Slot deleted successfully"}
