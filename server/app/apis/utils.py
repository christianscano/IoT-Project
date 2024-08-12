from functools import wraps
from flask import session
from app.utils import code_to_user_role

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