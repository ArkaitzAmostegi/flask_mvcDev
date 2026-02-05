from sqlalchemy import func
from app.extensions import db
from app.models.libro import Libro
from app.models.socio import Socio
from flask import abort
from app.models.libro import Libro

def listar_libros():
    return Libro.query.order_by(func.lower(Libro.titulo)).all()

def listar_disponibles():
    return Libro.query.filter(Libro.socio_id.is_(None)).order_by(func.lower(Libro.titulo)).all()

def buscar_por_titulo(titulo_parcial: str):
    patron = f"%{titulo_parcial}%"
    return Libro.query.filter(func.lower(Libro.titulo).like(func.lower(patron))).all()

def obtener_libro(id):
    return Libro.query.get(id)

def obtener_socio_por_codigo(codigo: str):
    return Socio.query.filter_by(codigo=codigo).first()

def crear_libro(titulo, autor, resumen=None, categoria=None, anio=None):
    libro = Libro(titulo=titulo, autor=autor, resumen=resumen, categoria=categoria, anio=anio)
    db.session.add(libro)
    db.session.commit()
    return libro

def editar_libro(libro_id, titulo=None, autor=None, resumen=None, categoria=None, anio=None):
    libro = Libro.query.get(libro_id)
    if not libro:
        return None
    if titulo is not None: libro.titulo = titulo
    if autor is not None: libro.autor = autor
    if resumen is not None: libro.resumen = resumen
    if categoria is not None: libro.categoria = categoria
    if anio is not None: libro.anio = anio
    db.session.commit()
    return libro

def prestar_libro(libro_id: int, socio_codigo: str):
    libro = Libro.query.get(libro_id)
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
    return Socio.query.join(Libro, Libro.socio_id == Socio.id).all()

def obtener_libro_o_404(libro_id: int) -> Libro:
    libro = Libro.query.get(libro_id)
    if not libro:
        abort(404)
    return libro
