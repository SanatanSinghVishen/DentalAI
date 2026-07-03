from app.services.availability import is_slot_available, suggest_alternatives

def test_is_slot_available_conflicts():
    existing = [
        {"date": "2023-10-20", "time": "10:00"}
    ]
    # Conflict within 30 mins
    assert not is_slot_available(existing, "2023-10-20", "10:15", buffer_min=30)
    assert not is_slot_available(existing, "2023-10-20", "09:45", buffer_min=30)
    
    # Valid slots outside 30 mins
    assert is_slot_available(existing, "2023-10-20", "10:30", buffer_min=30)
    assert is_slot_available(existing, "2023-10-20", "09:30", buffer_min=30)

def test_is_slot_available_outside_hours():
    existing = []
    # Before 9 AM
    assert not is_slot_available(existing, "2023-10-20", "08:30")
    # After 6 PM
    assert not is_slot_available(existing, "2023-10-20", "18:00")
    # Valid
    assert is_slot_available(existing, "2023-10-20", "14:00")

def test_is_slot_available_sunday():
    # 2023-10-22 is a Sunday
    existing = []
    assert not is_slot_available(existing, "2023-10-22", "10:00")

def test_suggest_alternatives():
    existing = [
        {"date": "2023-10-20", "time": "09:00"},
        {"date": "2023-10-20", "time": "09:30"},
        {"date": "2023-10-20", "time": "10:30"}
    ]
    
    alternatives = suggest_alternatives(existing, "2023-10-20", n=3)
    assert len(alternatives) == 3
    # 09:00 and 09:30 are taken. Next should be 10:00
    assert alternatives[0] == "10:00"
    # 10:30 is taken. Next should be 11:00
    assert alternatives[1] == "11:00"
    assert alternatives[2] == "11:30"
    
def test_suggest_alternatives_sunday():
    # 2023-10-22 is a Sunday
    existing = []
    alternatives = suggest_alternatives(existing, "2023-10-22", n=3)
    assert len(alternatives) == 0
