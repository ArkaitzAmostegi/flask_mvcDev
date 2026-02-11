from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def role_required(role: str):
    """Decorator que exige login y que el usuario tenga un rol concreto; si no, devuelve 403."""
    def decorator(fn):
        @wraps(fn)  # Mantiene nombre de la función original
        @login_required  # Obliga a estar autenticado antes de comprobar el rol
        def wrapper(*args, **kwargs):
            if getattr(current_user, "role", None) != role:  # Si el rol no coincide (o no existe), deniega acceso
                abort(403) 
            return fn(*args, **kwargs)  # Si todo OK, ejecuta la vista original
        return wrapper
    return decorator
