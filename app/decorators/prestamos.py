from functools import wraps
from flask import request, redirect, url_for, flash
from app.services.libros_service import obtener_libro

def validar_prestamo():
    """Decorator que valida antes de prestar: libro existente y socio_codigo informado."""
    def decorator(fn):
        @wraps(fn)  # Mantiene nombre de la función original
        def wrapper(*args, **kwargs):
            libro_id = kwargs.get("id")  # Lee el id del libro desde la ruta

            libro = obtener_libro(libro_id)  # Comprueba que el libro existe
            if not libro:
                flash("El libro no existe", "error")
                return redirect(url_for("libros.listar"))  # Vuelve al listado si el id no es válido

            socio_codigo = request.form.get("socio_codigo", "").strip()  # Lee el código del socio del formulario
            if not socio_codigo:
                flash("Debes indicar el código del socio", "error")
                return redirect(url_for("libros.detalle", id=libro_id))  # Vuelve al detalle para corregir

            return fn(*args, **kwargs)  # Si pasa validaciones, ejecuta la vista original
        return wrapper
    return decorator
