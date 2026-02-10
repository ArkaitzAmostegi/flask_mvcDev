from app.extensions import db
from app.models.socio import Socio
from app.models.libro import Libro
from app.services.libros_service import obtener_libro
from app.services.socios_service import obtener_socio_por_codigo


def prestar_libro(libro_id: int, socio_codigo: str):
    libro = obtener_libro(libro_id)
    if not libro:
        return (False, "El libro no existe")

    socio = obtener_socio_por_codigo(socio_codigo)
    if not socio:
        return (False, "El socio no existe")

    if libro.socio_id is not None:
        return (False, "El libro ya está prestado")

    if socio.libro_prestado is not None:
        return (False, "El socio ya tiene un libro")

    libro.socio_id = socio.id
    db.session.commit()
    return (True, "Préstamo realizado")


def devolver_por_socio(socio_codigo: str):
    socio = obtener_socio_por_codigo(socio_codigo)
    if not socio:
        return (False, "El socio no existe")

    if socio.libro_prestado is None:
        return (False, "El socio no tiene libro prestado")

    socio.libro_prestado.socio_id = None
    db.session.commit()
    return (True, "Devolución realizada")

def socios_con_prestamo():
    return (
        Socio.query
        .join(Libro, Libro.socio_id == Socio.id)
        .order_by(Socio.codigo.asc())
        .all()
    )
