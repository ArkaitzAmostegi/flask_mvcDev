from functools import wraps
from flask import redirect, url_for, flash
from app.services.libros_service import obtener_libro

def validar_prestamo():
    """Valida mínimo: el libro existe."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            libro_id = kwargs.get("id")

            libro = obtener_libro(libro_id)
            if not libro:
                flash("El libro no existe", "error")
                return redirect(url_for("libros.listar"))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
