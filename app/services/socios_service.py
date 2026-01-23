from app.extensions import db
from app.models.socio import Socio

def listar_socios():
    return Socio.query.order_by(Socio.codigo.asc()).all()

def obtener_socio(id: int):
    return Socio.query.get(id)

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
