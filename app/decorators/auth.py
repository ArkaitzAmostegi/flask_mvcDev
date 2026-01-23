from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def role_required(role: str):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if getattr(current_user, "role", None) != role:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
