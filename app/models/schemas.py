from pydantic import BaseModel
from typing import Optional, Literal

Service = Literal[
    "Dental Cleaning", "Root Canal Treatment", "Teeth Whitening",
    "Braces Consultation", "Tooth Extraction", "General Dental Consultation",
]

class CheckAvailabilityRequest(BaseModel):
    service: Service
    date: str   # YYYY-MM-DD
    time: str   # HH:MM, 24-hour

class CheckAvailabilityResponse(BaseModel):
    available: bool
    alternatives: list[str] = []

class BookAppointmentRequest(BaseModel):
    name: str
    phone: str
    service: Service
    date: str
    time: str
    call_id: str
    email: Optional[str] = None
    is_emergency: bool = False

class BookAppointmentResponse(BaseModel):
    status: Literal["confirmed", "failed"]
    booking_id: Optional[str] = None

class LogCallbackRequest(BaseModel):
    name: str
    phone: str
    reason: str
    call_id: str

class LogCallbackResponse(BaseModel):
    status: Literal["logged", "failed"]
