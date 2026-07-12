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

def test_check_availability_endpoint():
    from fastapi.testclient import TestClient
    from fastapi import Request
    from app.main import app
    from app.core.security import verify_retell_request
    
    async def mock_verify_retell_request(request: Request):
        return await request.json()
        
    app.dependency_overrides[verify_retell_request] = mock_verify_retell_request
    
    from unittest.mock import patch
    with patch("app.routers.functions.get_bookings_for_date", return_value=[]) as mock_get_bookings:
        try:
            client = TestClient(app)
            
            # 1. Valid request with all fields
            response = client.post(
                "/functions/check-availability",
                json={
                    "args": {
                        "service": "Dental Cleaning",
                        "date": "2026-07-20",
                        "time": "10:00"
                    }
                }
            )
            assert response.status_code == 200
            assert "available" in response.json()
            
            # 2. Request missing 'service' argument
            response_missing_service = client.post(
                "/functions/check-availability",
                json={
                    "args": {
                        "date": "2026-07-20",
                        "time": "10:00"
                    }
                }
            )
            assert response_missing_service.status_code == 200
            assert response_missing_service.json()["available"] is True
            
            # 3. Request with unrecognized service type
            response_bad_service = client.post(
                "/functions/check-availability",
                json={
                    "args": {
                        "service": "General Consultation",  # supposed to be 'General Dental Consultation'
                        "date": "2026-07-20",
                        "time": "10:00"
                    }
                }
            )
            assert response_bad_service.status_code == 200
            assert response_bad_service.json()["available"] is True
            
            assert mock_get_bookings.call_count == 3
        finally:
            app.dependency_overrides.clear()


