import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")

        if not re.search(r'[\W_]', password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return (
            "Your password must contain uppercase, lowercase, "
            "numbers, and special characters."
        )




BLOCKED_DOMAINS = [
    'mailinator.com', 
    'tempmail.com', 
    '10minutemail.com', 
    'yopmail.com',
    'sharklasers.com',
    'guerrillamailblock.com'
]

def validate_not_disposable_email(value):
    """Denies registration if the email domain is in the blocklist."""
    # Extract the domain (everything after the @ symbol)
    try:
        domain = value.split('@')[-1].lower()
    except IndexError:
        raise ValidationError("Invalid email format.")

    if domain in BLOCKED_DOMAINS:
        raise ValidationError("Registration using disposable email addresses is not allowed.")
