from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SlotBase(BaseModel):
    datetime: datetime
    duration_minutes: int = 60

class SlotCreate(SlotBase):
    tenant_id: int

class SlotBook(BaseModel):
    client_name: str
    client_email: EmailStr
    client_phone: Optional[str] = None
    client_message: Optional[str] = None

class SlotResponse(SlotBase):
    id: int
    is_booked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class SlotAdminResponse(SlotResponse):
    tenant_id: int
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_message: Optional[str] = None
    booked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SlotPublicResponse(SlotBase):
    id: int
    
    class Config:
        from_attributes = True

class BookingConfirmation(BaseModel):
    message: str
    slot_id: int
    datetime: datetime
    tenant_username: str
