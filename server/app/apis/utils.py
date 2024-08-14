from functools import wraps
from flask import session
from app.utils import code_to_user_role
import re


def auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'id' not in session:
            return "", 401
        return f(*args, **kwargs)
    return wrapper

def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if code_to_user_role(session.get('role')) != 'admin':
            return "", 403
        return f(*args, **kwargs)
    return wrapper

def security_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if code_to_user_role(session.get('role')) != 'security':
            return "", 403
        return f(*args, **kwargs)
    return wrapper

def validate_input(user_input):
    """
    Validates that the input contains only letters, numbers, and 
    allowed non-dangerous symbols.
    
    Allowed symbols: . - _ @ ! # $ % & * ?

    Parameters:
        user_input (str): The input string to be validated.
    
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    pattern = re.compile(r'^[\w\s.-_@!#$%&*?]*$')
    
    if pattern.match(user_input):
        return True
    return False