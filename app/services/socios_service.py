from app.extensions import db
from app.models.socio import Socio
from sqlalchemy import or_, func
from app.models.socio import Socio


def listar_socios():
    return Socio.query.order_by(Socio.codigo.asc()).all()

def obtener_socio(id: int):
    return Socio.query.get(id)

def obtener_socio_por_codigo(codigo: str):
    return Socio.query.filter_by(codigo=codigo).first()

def crear_socio(codigo: str, nombre: str, email: str):
    socio = Socio(codigo=codigo, nombre=nombre, email=email)
    db.session.add(socio)
    db.session.commit()
    return socio

def editar_socio(socio_id: int, codigo=None, nombre=None, email=None):
    socio = Socio.query.get(socio_id)
    if not socio:
        return None
    if codigo is not None: socio.codigo = codigo
    if nombre is not None: socio.nombre = nombre
    if email is not None: socio.email = email
    db.session.commit()
    return socio

def borrar_socio(socio_id: int):
    socio = Socio.query.get(socio_id)
    if not socio:
        return False, "El socio no existe"

    if socio.libro_prestado is not None:
        return False, "No se puede borrar: el socio tiene un libro prestado"

    db.session.delete(socio)
    db.session.commit()
    return True, "Socio borrado"

def buscar_socios(q: str):
    q = (q or "").strip()
    patron = f"%{q}%"
    return Socio.query.filter(
        or_(
            func.lower(Socio.nombre).like(func.lower(patron)),
            func.lower(Socio.email).like(func.lower(patron)),
        )
    ).order_by(func.lower(Socio.nombre)).all()