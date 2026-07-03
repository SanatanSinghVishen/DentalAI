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
            response = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                json={
                    "from": settings.CLINIC_FROM_EMAIL,
                    "to": settings.CLINIC_NOTIFY_EMAIL,
                    "subject": f"New booking: {booking['name']} - {booking['service']}",
                    "html": (
                        f"<p>{booking['name']} booked <strong>{booking['service']}</strong> on "
                        f"{booking['date']} at {booking['time']}.<br>"
                        f"Phone: {booking['phone']}</p>"
                    ),
                },
            )
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        # Note: We don't raise here because we don't want an email failure to cancel a successful booking.
