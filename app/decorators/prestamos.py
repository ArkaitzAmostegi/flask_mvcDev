from functools import wraps
from flask import redirect, url_for, flash
from app.models.libro import Libro
from app.models.socio import Socio

def validar_prestamo():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            libro_id = kwargs.get("id")
            socio_codigo = None

            # En POST viene del form
            from flask import request
            socio_codigo = request.form.get("socio_codigo")

            libro = Libro.query.get(libro_id)
            if not libro:
                flash("El libro no existe", "error")
                return redirect(url_for("libros.listar"))

            socio = Socio.query.filter_by(codigo=socio_codigo).first()
            if not socio:
                flash("El socio no existe", "error")
                return redirect(url_for("libros.detalle", id=libro_id))

            if libro.socio_id is not None:
                flash("El libro ya está prestado", "error")
                return redirect(url_for("libros.detalle", id=libro_id))

            if socio.libro_prestado is not None:
                flash("El socio ya tiene un libro", "error")
                return redirect(url_for("libros.detalle", id=libro_id))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
