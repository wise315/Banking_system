import re
import getpass
import time

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


def get_secure_password(prompt_message):
    """
    Prompts the user for a password while keeping keystrokes hidden.
    Enforces the strength test and limits failures to 3 attempts before a 10-second lockout.
    """
    attempts = 0
    while True:
        # getpass hides the keys as the user types them in the console
        password = getpass.getpass(prompt_message)
        
        if validate_password(password):
            return password
            
        attempts += 1
        if attempts >= 3:
            print("\n⛔ Too many weak password attempts! Please wait 10 seconds before trying again...")
            time.sleep(10)
            attempts = 0  # Reset counter after timeout penalty