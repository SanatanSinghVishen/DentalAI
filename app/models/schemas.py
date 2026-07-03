from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any

class CheckAvailabilityArgs(BaseModel):
    service: str
    date: str   # YYYY-MM-DD
    time: str   # HH:MM, 24-hour

class CheckAvailabilityRequest(BaseModel):
    args: CheckAvailabilityArgs

class CheckAvailabilityResponse(BaseModel):
    available: bool
    alternatives: list[str] = []

class BookAppointmentArgs(BaseModel):
    name: str
    phone: str
    service: str
    date: str
    time: str
    email: Optional[str] = None
    is_emergency: bool = False

class BookAppointmentRequest(BaseModel):
    call: Dict[str, Any]
    args: BookAppointmentArgs

class BookAppointmentResponse(BaseModel):
    status: Literal["confirmed", "failed"]
    booking_id: Optional[str] = None

class LogCallbackArgs(BaseModel):
    name: str
    phone: str
    reason: str

class LogCallbackRequest(BaseModel):
    call: Dict[str, Any]
    args: LogCallbackArgs

class LogCallbackResponse(BaseModel):
    status: Literal["logged", "failed"]
