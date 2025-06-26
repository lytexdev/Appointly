from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)  # URL slug
    display_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    
    # Page customization
    title = Column(String(200), default="Terminbuchung")
    description = Column(Text)
    primary_color = Column(String(7), default="#7F7FFF")  # Hex color
    logo_url = Column(String(500))
    
    # Business info
    business_name = Column(String(200))
    business_address = Column(Text)
    business_phone = Column(String(50))
    business_email = Column(String(255))
    
    # Settings
    is_active = Column(Boolean, default=True)
    allow_public_booking = Column(Boolean, default=True)
    booking_lead_time_hours = Column(Integer, default=24)  # Mindestvorlaufzeit
    max_advance_days = Column(Integer, default=30)  # Wie weit im Voraus buchbar
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tenants")
    slots = relationship("Slot", back_populates="tenant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tenant(username={self.username}, display_name={self.display_name})>"
