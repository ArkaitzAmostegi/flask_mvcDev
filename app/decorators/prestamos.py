# app/decorators/prestamos.py
from functools import wraps
from flask import request, redirect, url_for, flash
from app.services.libros_service import obtener_libro  


def validar_prestamo():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            libro_id = kwargs.get("id")

            # Validación mínima: el libro debe existir
            libro = obtener_libro(libro_id)
            if not libro:
                flash("El libro no existe", "error")
                return redirect(url_for("libros.listar"))

            # validar que venga el código
            socio_codigo = request.form.get("socio_codigo", "").strip()
            if not socio_codigo:
                flash("Debes indicar el código del socio", "error")
                return redirect(url_for("libros.detalle", id=libro_id))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
