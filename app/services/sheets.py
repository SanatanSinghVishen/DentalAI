import os
import json
import logging
from typing import List, Dict
import gspread
from google.oauth2.service_account import Credentials
from app.core.config import settings

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_client() -> gspread.Client:
    if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not set")
    
    info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_sheet_by_name(sheet_name: str) -> gspread.Worksheet:
    if not settings.GOOGLE_SHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID is not set")
        
    client = get_client()
    return client.open_by_key(settings.GOOGLE_SHEET_ID).worksheet(sheet_name)

def append_booking(row: dict):
    try:
        sheet = get_sheet_by_name("Bookings")
        sheet.append_row([
            row.get("timestamp", ""),
            row.get("booking_id", ""),
            row.get("name", ""),
            row.get("phone", ""),
            row.get("email", ""),
            row.get("service", ""),
            row.get("date", ""),
            row.get("time", ""),
            row.get("status", ""),
            row.get("is_emergency", False),
            row.get("call_id", ""),
        ])
    except Exception as e:
        logger.error(f"Failed to append booking to sheets: {e}")
        raise

def get_bookings_for_date(date: str) -> List[Dict]:
    try:
        if not settings.GOOGLE_SERVICE_ACCOUNT_JSON or not settings.GOOGLE_SHEET_ID:
            return []
            
        sheet = get_sheet_by_name("Bookings")
        all_records = sheet.get_all_records()
        return [r for r in all_records if str(r.get("date", "")) == date]
    except Exception as e:
        logger.error(f"Failed to fetch bookings for date {date}: {e}")
        return []

def append_callback(row: dict):
    try:
        sheet = get_sheet_by_name("Callbacks")
        sheet.append_row([
            row.get("timestamp", ""),
            row.get("name", ""),
            row.get("phone", ""),
            row.get("reason", ""),
            row.get("call_id", ""),
        ])
    except Exception as e:
        logger.error(f"Failed to append callback to sheets: {e}")
        raise
