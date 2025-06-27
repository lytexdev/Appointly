from datetime import datetime
from utils.email.smtp import send_email
from models.tenants import Tenant
from models.slot import Slot
from utils.email.templates import render_booking_confirmation, render_admin_notification
from config.settings import settings

class EmailService:
    @staticmethod
    async def send_booking_confirmation(slot: Slot):
        """Send booking confirmation email to client"""
        appointment_date = slot.datetime.strftime("%d.%m.%Y")
        appointment_time = slot.datetime.strftime("%H:%M")
        
        html_content = render_booking_confirmation(
            client_name=slot.client_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            duration=slot.duration_minutes,
            client_message=slot.client_message,
            app_name=settings.APP_NAME
        )
        
        subject = f"Terminbestätigung - {appointment_date} um {appointment_time}"
        
        return await send_email(
            to_email=slot.client_email,
            subject=subject,
            html_content=html_content
        )
    
    @staticmethod
    async def send_admin_notification(slot: Slot):
        """Send booking notification email to admin"""
        appointment_date = slot.datetime.strftime("%d.%m.%Y")
        appointment_time = slot.datetime.strftime("%H:%M")
        
        html_content = render_admin_notification(
            client_name=slot.client_name,
            client_email=slot.client_email,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            duration=slot.duration_minutes,
            slot_id=slot.id,
            client_message=slot.client_message,
            app_name=settings.APP_NAME
        )
        
        subject = f"Neue Terminbuchung - {slot.client_name} ({appointment_date})"
        
        return await send_email(
            to_email=settings.ADMIN_EMAIL,
            subject=subject,
            html_content=html_content
        )