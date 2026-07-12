from datetime import datetime

def is_slot_available(existing: list[dict], date: str, time: str, buffer_min=30) -> bool:
    try:
        requested = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return False
        
    for b in existing:
        try:
            booked = datetime.strptime(f"{b['date']} {b['time']}", "%Y-%m-%d %H:%M")
            if abs((requested - booked).total_seconds()) < buffer_min * 60:
                return False
        except (ValueError, KeyError):
            continue
            
    if requested.hour < 9 or requested.hour >= 18:
        return False
        
    if requested.weekday() == 6:
        return False

    return True

def suggest_alternatives(existing: list[dict], date: str, n: int = 3) -> list[str]:
    booked_times = {b["time"] for b in existing if b.get("date") == date}
    
    try:
        req_date = datetime.strptime(date, "%Y-%m-%d")
        if req_date.weekday() == 6:
            return []
    except ValueError:
        pass
        
    slots, hour = [], 9
    while hour < 18 and len(slots) < n:
        for minute in (0, 30):
            candidate = f"{hour:02d}:{minute:02d}"
            if is_slot_available(existing, date, candidate):
                slots.append(candidate)
            if len(slots) >= n:
                break
        hour += 1
    return slots

def normalize_service(service: str) -> str:
    s = service.lower().strip()
    if "root" in s or "canal" in s:
        return "Root Canal Treatment"
    if "cleaning" in s:
        return "Dental Cleaning"
    if "whitening" in s:
        return "Teeth Whitening"
    if "brace" in s:
        return "Braces Consultation"
    if "extract" in s:
        return "Tooth Extraction"
    if "consult" in s:
        return "General Dental Consultation"
    return service.strip().title()

def clean_email(email: str | None) -> str | None:
    if not email:
        return None
        
    s = email.lower().strip()
    
    # Replace common verbalizations
    s = s.replace("at the rate", "@")
    
    # Replace "at" if "@" is not already present
    if "@" not in s:
        s = s.replace(" at ", "@")
        
    # Replace "dot" with "."
    s = s.replace("dot", ".")
    
    # Remove all whitespace (since emails don't contain spaces)
    s = "".join(s.split())
    
    return s

