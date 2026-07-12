_seen: set[str] = set()

def already_processed(key: str) -> bool:
    if key in _seen:
        return True
    _seen.add(key)
    return False

def clear_cache():
    _seen.clear()
