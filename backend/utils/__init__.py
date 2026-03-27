"""Input validation and sanitization utilities."""
import re
import html


VALID_TRAVEL_MODES = {'car', 'bus', 'bike', 'walking'}
VALID_FOOD_HABITS = {'veg', 'non-veg', 'vegan'}
VALID_ROLES = {'student', 'admin'}


def sanitize_string(value):
    """Escape HTML entities to prevent XSS."""
    if not isinstance(value, str):
        return ''
    return html.escape(value.strip(), quote=True)


def validate_email(email):
    """Validate email format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_password(password):
    """Validate password strength (min 8 chars, at least 1 letter and 1 digit)."""
    if not password or not isinstance(password, str):
        return False, 'Password is required.'
    if len(password) < 8:
        return False, 'Password must be at least 8 characters.'
    if not re.search(r'[A-Za-z]', password):
        return False, 'Password must contain at least one letter.'
    if not re.search(r'\d', password):
        return False, 'Password must contain at least one digit.'
    return True, 'OK'


def validate_username(username):
    """Validate username (3-30 chars, alphanumeric + underscores)."""
    if not username or not isinstance(username, str):
        return False, 'Username is required.'
    username = username.strip()
    if len(username) < 3 or len(username) > 30:
        return False, 'Username must be 3–30 characters.'
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, 'Username can only contain letters, numbers, and underscores.'
    return True, 'OK'


def validate_carbon_entry(data):
    """Validate carbon entry input data.

    Returns:
        (is_valid, error_message, cleaned_data)
    """
    errors = []
    cleaned = {}

    # Travel mode
    travel_mode = data.get('travel_mode', '').strip().lower()
    if travel_mode not in VALID_TRAVEL_MODES:
        errors.append(f'Invalid travel mode. Must be one of: {", ".join(VALID_TRAVEL_MODES)}')
    cleaned['travel_mode'] = travel_mode

    # Distance
    try:
        distance = float(data.get('distance', 0))
        if distance < 0 or distance > 1000:
            errors.append('Distance must be between 0 and 1000 km.')
        cleaned['distance'] = distance
    except (ValueError, TypeError):
        errors.append('Distance must be a valid number.')
        cleaned['distance'] = 0

    # Electricity usage
    try:
        electricity = float(data.get('electricity_usage', 0))
        if electricity < 0 or electricity > 500:
            errors.append('Electricity usage must be between 0 and 500 units.')
        cleaned['electricity_usage'] = electricity
    except (ValueError, TypeError):
        errors.append('Electricity usage must be a valid number.')
        cleaned['electricity_usage'] = 0

    # Food habit
    food_habit = data.get('food_habit', '').strip().lower()
    if food_habit not in VALID_FOOD_HABITS:
        errors.append(f'Invalid food habit. Must be one of: {", ".join(VALID_FOOD_HABITS)}')
    cleaned['food_habit'] = food_habit

    if errors:
        return False, '; '.join(errors), cleaned
    return True, 'OK', cleaned
