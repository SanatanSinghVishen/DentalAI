# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any

# Valid services offered by the clinic
ServiceType = Literal[
    "Dental Cleaning",
    "Root Canal Treatment",
    "Teeth Whitening",
    "Braces Consultation",
    "Tooth Extraction",
    "General Dental Consultation",
]

class CheckAvailabilityArgs(BaseModel):
    date: str   # YYYY-MM-DD
    time: str   # HH:MM, 24-hour
    service: Optional[str] = None

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
    is_emergency: Optional[bool] = False

class BookAppointmentRequest(BaseModel):
    call: Dict[str, Any]
    args: BookAppointmentArgs

class BookAppointmentResponse(BaseModel):
    status: Literal["confirmed", "failed"]
    booking_id: Optional[str] = None

class LogCallbackArgs(BaseModel):
    reason: str
    name: Optional[str] = None
    phone: Optional[str] = None

class LogCallbackRequest(BaseModel):
    call: Dict[str, Any]
    args: LogCallbackArgs

class LogCallbackResponse(BaseModel):
    status: Literal["logged", "failed"]

class EscalateArgs(BaseModel):
    reason_for_escalation: str
    is_emergency: bool

class EscalateRequest(BaseModel):
    call: Dict[str, Any]
    args: EscalateArgs

class EscalateResponse(BaseModel):
    escalation_approved: bool = True
    transfer_number: str = "8957428488"
