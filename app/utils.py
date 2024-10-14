from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)


def validate_todo_data(data):
    """Data validation for todo creation"""
    if not data or 'title' not in data or not data['title'].strip():
        return False, "Title name must not be empty."
    return True, None
