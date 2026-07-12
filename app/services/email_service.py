# pyrefly: ignore [missing-import]
import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_internal_notification(booking: dict):
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not configured. Skipping email notification.")
        return

    try:
        async with httpx.AsyncClient() as client:
            recipients = [settings.CLINIC_NOTIFY_EMAIL]
            if booking.get("email"):
                recipients.append(booking["email"])
                
            response = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                json={
                    "from": settings.CLINIC_FROM_EMAIL,
                    "to": recipients,
                    "subject": f"Appointment Confirmed: {booking['name']} - {booking['service']}",
                    "html": (
                        f"<p>Hello {booking['name']},</p>"
                        f"<p>Your appointment for <strong>{booking['service']}</strong> is confirmed on "
                        f"{booking['date']} at {booking['time']}.</p>"
                        f"<p>We will reach you at {booking['phone']} if needed.</p>"
                        f"<p>Thank you,<br>QuensultingAI Dental Clinic</p>"
                    ),
                },
            )
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
