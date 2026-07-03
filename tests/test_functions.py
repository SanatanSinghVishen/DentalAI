import pytest
from pydantic import ValidationError
from app.models.schemas import BookAppointmentRequest, BookAppointmentArgs
from app.services.idempotency import already_processed, clear_cache

def test_book_appointment_request_schema():
    # Valid request
    req = BookAppointmentRequest(
        call={"call_id": "call_123"},
        args=BookAppointmentArgs(
            name="John Doe",
            phone="1234567890",
            service="Dental Cleaning",
            date="2023-10-20",
            time="10:00"
        )
    )
    assert req.args.service == "Dental Cleaning"
    
    # Invalid service enum
    with pytest.raises(ValidationError):
        BookAppointmentRequest(
            call={"call_id": "call_123"},
            args=BookAppointmentArgs(
                name="John Doe",
                phone="1234567890",
                service="Fake Service",
                date="2023-10-20",
                time="10:00"
            )
        )

def test_idempotency_logic():
    clear_cache()
    
    key = "call_abc:book_appointment"
    
    # First time should return False
    assert not already_processed(key)
    
    # Second time should return True
    assert already_processed(key)
    
    # Third time should return True
    assert already_processed(key)
