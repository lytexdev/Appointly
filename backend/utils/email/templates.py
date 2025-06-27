from jinja2 import Template

BOOKING_CONFIRMATION_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Terminbestätigung - {{ business_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: {{ primary_color or '#4CAF50' }}; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .details { background-color: white; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ tenant_title }}</h1>
            <h2>{{ business_name }}</h2>
        </div>
        <div class="content">
            <p>Hallo {{ client_name }},</p>
            <p>vielen Dank für Ihre Terminbuchung! Hiermit bestätigen wir Ihren Termin:</p>
            
            <div class="details">
                <h3>Termindetails:</h3>
                <p><strong>Datum:</strong> {{ appointment_date }}</p>
                <p><strong>Uhrzeit:</strong> {{ appointment_time }}</p>
                <p><strong>Dauer:</strong> {{ duration }} Minuten</p>
                {% if client_message %}
                <p><strong>Ihre Nachricht:</strong> {{ client_message }}</p>
                {% endif %}
            </div>
            
            <p>Falls Sie Fragen haben oder den Termin ändern müssen, kontaktieren Sie uns bitte.</p>
            <p>Wir freuen uns auf Ihren Besuch!</p>
        </div>
        <div class="footer">
            <p>{{ business_name }} - Powered by Appointly</p>
        </div>
    </div>
</body>
</html>
""")

ADMIN_NOTIFICATION_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Neue Terminbuchung - {{ business_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .details { background-color: white; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Neue Terminbuchung</h1>
            <h2>{{ business_name }}</h2>
        </div>
        <div class="content">
            <p>Es wurde ein neuer Termin für {{ tenant_username }} gebucht:</p>
            
            <div class="details">
                <h3>Kundendaten:</h3>
                <p><strong>Name:</strong> {{ client_name }}</p>
                <p><strong>E-Mail:</strong> {{ client_email }}</p>
                {% if client_phone %}
                <p><strong>Telefon:</strong> {{ client_phone }}</p>
                {% endif %}
                {% if client_message %}
                <p><strong>Nachricht:</strong> {{ client_message }}</p>
                {% endif %}
            </div>
            
            <div class="details">
                <h3>Termindetails:</h3>
                <p><strong>Datum:</strong> {{ appointment_date }}</p>
                <p><strong>Uhrzeit:</strong> {{ appointment_time }}</p>
                <p><strong>Dauer:</strong> {{ duration }} Minuten</p>
                <p><strong>Slot-ID:</strong> {{ slot_id }}</p>
            </div>
        </div>
        <div class="footer">
            <p>{{ business_name }} - Appointly Admin-Benachrichtigung</p>
        </div>
    </div>
</body>
</html>
""")

def render_booking_confirmation(
    client_name: str,
    appointment_date: str,
    appointment_time: str,
    duration: int,
    business_name: str,
    tenant_title: str,
    primary_color: str = "#4CAF50",
    client_message: str = None
) -> str:
    return BOOKING_CONFIRMATION_TEMPLATE.render(
        client_name=client_name,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        duration=duration,
        client_message=client_message,
        business_name=business_name,
        tenant_title=tenant_title,
        primary_color=primary_color
    )

def render_admin_notification(
    client_name: str,
    client_email: str,
    appointment_date: str,
    appointment_time: str,
    duration: int,
    slot_id: int,
    business_name: str,
    tenant_username: str,
    client_phone: str = None,
    client_message: str = None
) -> str:
    return ADMIN_NOTIFICATION_TEMPLATE.render(
        client_name=client_name,
        client_email=client_email,
        client_phone=client_phone,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        duration=duration,
        slot_id=slot_id,
        client_message=client_message,
        business_name=business_name,
        tenant_username=tenant_username
    )
