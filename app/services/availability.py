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
            
    # Check if requested time is outside working hours (9 AM to 6 PM)
    if requested.hour < 9 or requested.hour >= 18:
        return False
        
    # Check if requested time is Sunday (6 = Sunday in Python's weekday(), where Monday is 0)
    if requested.weekday() == 6:
        return False

    return True

def suggest_alternatives(existing: list[dict], date: str, n: int = 3) -> list[str]:
    booked_times = {b["time"] for b in existing if b.get("date") == date}
    
    # Simple check for Sunday
    try:
        req_date = datetime.strptime(date, "%Y-%m-%d")
        if req_date.weekday() == 6:
            return [] # No slots on Sunday
    except ValueError:
        pass
        
    slots, hour = [], 9
    while hour < 18 and len(slots) < n:
        for minute in (0, 30):
            candidate = f"{hour:02d}:{minute:02d}"
            # Let's verify it against existing bookings more robustly than just exact time match
            if is_slot_available(existing, date, candidate):
                slots.append(candidate)
            if len(slots) >= n:
                break
        hour += 1
    return slots
