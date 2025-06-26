from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
from datetime import datetime

class Slot(Base):
    __tablename__ = "slots"
    
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=60)
    is_booked = Column(Boolean, default=False)
    
    # Tenant relationship
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="slots")
    
    # Booking information
    client_name = Column(String(100), nullable=True)
    client_email = Column(String(255), nullable=True)
    client_phone = Column(String(50), nullable=True)
    client_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    booked_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Slot(id={self.id}, tenant_id={self.tenant_id}, datetime={self.datetime}, is_booked={self.is_booked})>"
