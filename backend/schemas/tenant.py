from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
import re

class TenantBase(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    title: str = "Terminbuchung"
    description: Optional[str] = None
    primary_color: str = "#7F7FFF"
    logo_url: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_phone: Optional[str] = None
    business_email: Optional[EmailStr] = None
    allow_public_booking: bool = True
    booking_lead_time_hours: int = 24
    max_advance_days: int = 30

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return v.lower()

    @validator('primary_color')
    def validate_color(cls, v):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Primary color must be a valid hex color code')
        return v

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = None
    logo_url: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_phone: Optional[str] = None
    business_email: Optional[EmailStr] = None
    allow_public_booking: Optional[bool] = None
    booking_lead_time_hours: Optional[int] = None
    max_advance_days: Optional[int] = None

class TenantPublic(BaseModel):
    username: str
    display_name: str
    title: str
    description: Optional[str] = None
    primary_color: str
    logo_url: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_phone: Optional[str] = None
    business_email: Optional[str] = None
    allow_public_booking: bool
    booking_lead_time_hours: int
    max_advance_days: int

    class Config:
        from_attributes = True

class TenantResponse(TenantPublic):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TenantAdminResponse(TenantResponse):
    owner_id: int
    
    class Config:
        from_attributes = True
