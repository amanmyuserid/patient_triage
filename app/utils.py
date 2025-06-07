def is_valid_mobile(mobile: str) -> bool:
    return mobile.isdigit() and len(mobile) == 10 and mobile.startswith(("6", "7", "8", "9"))