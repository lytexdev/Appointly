from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.slot import Slot
from models.tenants import Tenant
from schemas.slot import SlotCreate, SlotBook
from services.email_service import EmailService
from fastapi import HTTPException, status

class SlotService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_available_slots_for_tenant(self, tenant_username: str) -> List[Slot]:
        """Get all available (not booked) slots for a specific tenant"""
        tenant = self.db.query(Tenant).filter(
            and_(
                Tenant.username == tenant_username.lower(),
                Tenant.is_active == True,
                Tenant.allow_public_booking == True
            )
        ).first()
        
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found or booking disabled"
            )
        
        # Calculate time constraints
        now = datetime.now()
        min_booking_time = now + timedelta(hours=tenant.booking_lead_time_hours)
        max_booking_time = now + timedelta(days=tenant.max_advance_days)
        
        return self.db.query(Slot).filter(
            and_(
                Slot.tenant_id == tenant.id,
                Slot.is_booked == False,
                Slot.datetime >= min_booking_time,
                Slot.datetime <= max_booking_time
            )
        ).order_by(Slot.datetime).all()
    
    def get_tenant_slots(self, tenant_id: int) -> List[Slot]:
        """Get all slots for a tenant (owner/admin view)"""
        return self.db.query(Slot).filter(
            Slot.tenant_id == tenant_id
        ).order_by(Slot.datetime.desc()).all()
    
    def get_all_slots(self) -> List[Slot]:
        """Get all slots (super admin view)"""
        return self.db.query(Slot).order_by(Slot.datetime.desc()).all()
    
    def get_slot_by_id(self, slot_id: int) -> Optional[Slot]:
        """Get slot by ID"""
        return self.db.query(Slot).filter(Slot.id == slot_id).first()
    
    def create_slot(self, slot_data: SlotCreate, user_id: int) -> Slot:
        """Create a new slot (only by tenant owner or admin)"""
        tenant = self.db.query(Tenant).filter(Tenant.id == slot_data.tenant_id).first()
        
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        
        # Check if user owns this tenant (or is admin)
        from models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user.is_admin and tenant.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create slots for this tenant"
            )
        
        slot = Slot(
            datetime=slot_data.datetime,
            duration_minutes=slot_data.duration_minutes,
            tenant_id=slot_data.tenant_id
        )
        
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot
    
    async def book_slot(self, slot_id: int, booking_data: SlotBook, tenant_username: str) -> Optional[Slot]:
        """Book a slot for a specific tenant"""
        # Get tenant first
        tenant = self.db.query(Tenant).filter(
            and_(
                Tenant.username == tenant_username.lower(),
                Tenant.is_active == True,
                Tenant.allow_public_booking == True
            )
        ).first()
        
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found or booking disabled"
            )
        
        # Get slot
        slot = self.db.query(Slot).filter(
            and_(
                Slot.id == slot_id,
                Slot.tenant_id == tenant.id
            )
        ).first()
        
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )
        
        if slot.is_booked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot is already booked"
            )
        
        # Check timing constraints
        now = datetime.now()
        min_booking_time = now + timedelta(hours=tenant.booking_lead_time_hours)
        
        if slot.datetime <= min_booking_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slot must be booked at least {tenant.booking_lead_time_hours} hours in advance"
            )
        
        # Update slot with booking information
        slot.is_booked = True
        slot.client_name = booking_data.client_name
        slot.client_email = booking_data.client_email
        slot.client_phone = booking_data.client_phone
        slot.client_message = booking_data.client_message
        slot.booked_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(slot)
        
        # Send emails
        try:
            await EmailService.send_booking_confirmation(slot, tenant)
            await EmailService.send_admin_notification(slot, tenant)
        except Exception as e:
            # Log error but don't rollback the booking
            print(f"Failed to send emails: {e}")
        
        return slot
    
    def delete_slot(self, slot_id: int, user_id: int) -> bool:
        """Delete a slot (only by tenant owner or admin)"""
        slot = self.get_slot_by_id(slot_id)
        
        if not slot:
            return False
        
        # Check if user owns this tenant (or is admin)
        from models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        tenant = self.db.query(Tenant).filter(Tenant.id == slot.tenant_id).first()
        
        if not user.is_admin and tenant.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this slot"
            )
        
        self.db.delete(slot)
        self.db.commit()
        return True