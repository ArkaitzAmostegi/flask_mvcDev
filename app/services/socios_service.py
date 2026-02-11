from app.extensions import db
from sqlalchemy import or_, func
from app.models.socio import Socio
from app.models.libro import Libro


def listar_socios():
    """Devuelve todos los socios ordenados por código."""
    return Socio.query.order_by(Socio.codigo.asc()).all()


def obtener_socio(socio_id: int):
    """Devuelve un socio por id o None si no existe."""
    return Socio.query.get(socio_id)


def obtener_socio_por_codigo(codigo: str):
    """Devuelve un socio por su código (único) o None si no existe."""
    return Socio.query.filter_by(codigo=codigo).first()


def crear_socio(codigo: str, nombre: str, email: str):
    """Crea y guarda un socio nuevo en la base de datos."""
    socio = Socio(codigo=codigo, nombre=nombre, email=email)
    db.session.add(socio)
    db.session.commit()
    return socio


def editar_socio(socio_id: int, codigo=None, nombre=None, email=None):
    """Actualiza datos del socio indicado (solo los campos que vengan) y guarda cambios."""
    socio = Socio.query.get(socio_id)
    if not socio:
        return None

    if codigo is not None:
        socio.codigo = codigo
    if nombre is not None:
        socio.nombre = nombre
    if email is not None:
        socio.email = email

    db.session.commit()
    return socio


def borrar_socio(socio_id: int):
    """Borra un socio si existe y no tiene un libro prestado; devuelve (ok, mensaje)."""
    socio = Socio.query.get(socio_id)
    if not socio:
        return False, "El socio no existe"

    if socio.libro_prestado is not None:
        return False, "No se puede borrar: el socio tiene un libro prestado"

    db.session.delete(socio)
    db.session.commit()
    return True, "Socio borrado"


def buscar_socios(q: str):
    """Busca socios por nombre o email (búsqueda parcial, sin distinguir mayúsculas/minúsculas)."""
    q = (q or "").strip()
    patron = f"%{q}%"
    return (
        Socio.query
        .filter(
            or_(
                func.lower(Socio.nombre).like(func.lower(patron)),
                func.lower(Socio.email).like(func.lower(patron)),
            )
        )
        .order_by(func.lower(Socio.nombre))
        .all()
    )


def socios_con_prestamo():
    """Devuelve los socios que tienen un libro prestado (join con Libro por socio_id)."""
    return (
        Socio.query
        .join(Libro, Libro.socio_id == Socio.id)
        .order_by(Socio.codigo.asc())
        .all()
    )
