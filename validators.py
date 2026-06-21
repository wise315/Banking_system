import re

def validate_password(password):
    """Rejects weak passwords based on length, numbers, and special characters."""
    if len(password) < 8:
        print("❌ Password must be at least 8 characters long.")
        return False
    if not re.search(r"\d", password):
        print("❌ Password must contain at least one number.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<> ]", password):
        print("❌ Password must contain at least one special character.")
        return False
    return True