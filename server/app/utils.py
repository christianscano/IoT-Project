from functools import wraps
from flask import session, redirect, url_for


def auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('frontend.index'))
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


def user_role_to_code(role):
    if role == 'admin':
        return 0
    elif role == 'security':
        return 1
    elif role == 'sysadmin':
        return 2
    else:
        return -1


def code_to_user_role(role):
    if role == 0:
        return 'admin'
    elif role == 1:
        return 'security'
    elif role == 2:
        return 'sysadmin'
    else:
        return 'unknown'