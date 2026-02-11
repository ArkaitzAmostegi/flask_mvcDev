# app/services/prestamos_service.py
from app.extensions import db
from app.services.libros_service import obtener_libro
from app.services.socios_service import obtener_socio_por_codigo
from app.services.socios_service import socios_con_prestamo as socios_con_prestamo_service


def socios_con_prestamo():
    """Devuelve la lista de socios que tienen un préstamo activo (delegando al servicio de socios)."""
    return socios_con_prestamo_service()


def prestar_libro(libro_id: int, socio_codigo: str):
    """Asigna un libro a un socio (préstamo) si existen y cumplen las reglas; devuelve (ok, mensaje)."""
    libro = obtener_libro(libro_id)
    if not libro:
        return False, "El libro no existe"

    socio = obtener_socio_por_codigo(socio_codigo)
    if not socio:
        return False, "El socio no existe"

    if libro.socio_id is not None:
        return False, "El libro ya está prestado"

    if socio.libro_prestado is not None:
        return False, "El socio ya tiene un libro"

    libro.socio_id = socio.id
    db.session.commit()
    return True, "Préstamo realizado"


def devolver_por_socio(socio_codigo: str):
    """Devuelve el libro prestado por el socio indicado; devuelve (ok, mensaje)."""
    socio = obtener_socio_por_codigo(socio_codigo)
    if not socio:
        return False, "El socio no existe"

    if socio.libro_prestado is None:
        return False, "El socio no tiene libro prestado"

    socio.libro_prestado.socio_id = None
    db.session.commit()
    return True, "Devolución realizada"
