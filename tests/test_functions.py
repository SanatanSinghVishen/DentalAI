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
    
    # Fuzzy service names are accepted by the schema
    req_fuzzy = BookAppointmentRequest(
        call={"call_id": "call_123"},
        args=BookAppointmentArgs(
            name="John Doe",
            phone="1234567890",
            service="Root Canal",
            date="2023-10-20",
            time="10:00"
        )
    )
    assert req_fuzzy.args.service == "Root Canal"

def test_normalize_service():
    from app.services.availability import normalize_service
    
    assert normalize_service("Root Canal") == "Root Canal Treatment"
    assert normalize_service("root canal") == "Root Canal Treatment"
    assert normalize_service("cleaning") == "Dental Cleaning"
    assert normalize_service("dental cleaning") == "Dental Cleaning"
    assert normalize_service("whitening") == "Teeth Whitening"
    assert normalize_service("brace") == "Braces Consultation"
    assert normalize_service("extraction") == "Tooth Extraction"
    assert normalize_service("general consultation") == "General Dental Consultation"
    assert normalize_service("Some Random Service") == "Some Random Service"

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

def test_escalate_endpoint():
    from fastapi.testclient import TestClient
    from fastapi import Request
    from app.main import app
    from app.core.security import verify_retell_request
    from unittest.mock import patch
    
    async def mock_verify_retell_request(request: Request):
        return await request.json()
        
    app.dependency_overrides[verify_retell_request] = mock_verify_retell_request
    
    with patch("app.routers.functions.append_callback") as mock_append_callback:
        try:
            client = TestClient(app)
            
            response = client.post(
                "/functions/escalate",
                json={
                    "call": {"call_id": "call_999", "from_number": "+12223334444"},
                    "args": {
                        "reason_for_escalation": "Patient reports severe bleeding after wisdom tooth extraction",
                        "is_emergency": True
                    }
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["escalation_approved"] is True
            assert data["transfer_number"] == "8957428488"
            
            mock_append_callback.assert_called_once()
            called_row = mock_append_callback.call_args[0][0]
            assert called_row["phone"] == "+12223334444"
            assert "Patient reports severe bleeding" in called_row["reason"]
        finally:
            app.dependency_overrides.clear()

def test_log_callback_endpoint_validation():
    from fastapi.testclient import TestClient
    from fastapi import Request
    from app.main import app
    from app.core.security import verify_retell_request
    from unittest.mock import patch
    
    async def mock_verify_retell_request(request: Request):
        return await request.json()
        
    app.dependency_overrides[verify_retell_request] = mock_verify_retell_request
    
    with patch("app.routers.functions.append_callback") as mock_append_callback:
        try:
            client = TestClient(app)
            
            # 1. Post request missing name and phone in args (should fail with 422)
            response_invalid = client.post(
                "/functions/log-callback-request",
                json={
                    "call": {"call_id": "call_888", "from_number": "+19998887777"},
                    "args": {
                        "reason": "Request callback for emergency pain relief"
                    }
                }
            )
            assert response_invalid.status_code == 422
            
            # 2. Post request with required name and phone (should succeed with 200)
            response_valid = client.post(
                "/functions/log-callback-request",
                json={
                    "call": {"call_id": "call_888", "from_number": "+19998887777"},
                    "args": {
                        "name": "Jane Doe",
                        "phone": "+19998887777",
                        "reason": "Request callback for emergency pain relief"
                    }
                }
            )
            assert response_valid.status_code == 200
            assert response_valid.json()["status"] == "logged"
            
            mock_append_callback.assert_called_once()
            called_row = mock_append_callback.call_args[0][0]
            assert called_row["name"] == "Jane Doe"
            assert called_row["phone"] == "+19998887777"
            assert called_row["reason"] == "Request callback for emergency pain relief"
        finally:
            app.dependency_overrides.clear()


