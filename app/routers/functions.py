import uuid
import logging
from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import (
    CheckAvailabilityRequest, CheckAvailabilityResponse,
    BookAppointmentRequest, BookAppointmentResponse,
    LogCallbackRequest, LogCallbackResponse
)
from app.core.security import verify_retell_request
from app.services.sheets import get_bookings_for_date, append_booking, append_callback
from app.services.availability import is_slot_available, suggest_alternatives
from app.services.idempotency import already_processed
from app.services.email_service import send_internal_notification

router = APIRouter(dependencies=[Depends(verify_retell_request)])
logger = logging.getLogger(__name__)

_booking_cache = {}

@router.post("/check-availability", response_model=CheckAvailabilityResponse)
async def check_availability(request: CheckAvailabilityRequest):
    args = request.args
    existing_bookings = get_bookings_for_date(args.date)
    
    available = is_slot_available(existing_bookings, args.date, args.time)
    alternatives = []
    
    if not available:
        alternatives = suggest_alternatives(existing_bookings, args.date)
        
    return CheckAvailabilityResponse(
        available=available,
        alternatives=alternatives
    )

@router.post("/book-appointment", response_model=BookAppointmentResponse)
async def book_appointment(request: BookAppointmentRequest):
    args = request.args
    call_id = request.call.get("call_id", "unknown")
    idempotency_key = f"{call_id}:book_appointment"
    
    if already_processed(idempotency_key):
        if idempotency_key in _booking_cache:
            return _booking_cache[idempotency_key]
            
    booking_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    row_data = {
        "timestamp": timestamp,
        "booking_id": booking_id,
        "name": args.name,
        "phone": args.phone,
        "email": args.email,
        "service": args.service,
        "date": args.date,
        "time": args.time,
        "status": "confirmed",
        "is_emergency": args.is_emergency or False,
        "call_id": call_id
    }
    
    try:
        append_booking(row_data)
        await send_internal_notification(row_data)
        
        response = BookAppointmentResponse(status="confirmed", booking_id=booking_id)
        _booking_cache[idempotency_key] = response
        return response
        
    except Exception as e:
        logger.error(f"Failed to book appointment: {e}")
        return BookAppointmentResponse(status="failed", booking_id=None)

@router.post("/log-callback-request", response_model=LogCallbackResponse)
async def log_callback_request(request: LogCallbackRequest):
    args = request.args
    call_id = request.call.get("call_id", "unknown")
    timestamp = datetime.now(timezone.utc).isoformat()
    
    row_data = {
        "timestamp": timestamp,
        "name": args.name,
        "phone": args.phone,
        "reason": args.reason,
        "call_id": call_id
    }
    
    try:
        append_callback(row_data)
        return LogCallbackResponse(status="logged")
    except Exception as e:
        logger.error(f"Failed to log callback request: {e}")
        return LogCallbackResponse(status="failed")
