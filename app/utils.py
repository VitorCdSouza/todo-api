def validate_todo_data(data):
    """Data validation for todo creation"""
    if not data or 'title' not in data or not data['title'].strip():
        return False, "Title name must not be empty."
    return True, None
