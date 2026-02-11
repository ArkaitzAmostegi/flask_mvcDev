from sqlalchemy import func
from flask import abort
from app.extensions import db
from app.models.libro import Libro


def borrar_libro(libro_id: int):
    """Borra un libro si existe y no está prestado; devuelve (ok, mensaje)."""
    libro = Libro.query.get(libro_id)
    if not libro:
        return False, "El libro no existe"

    if libro.socio_id is not None:
        return False, "No se puede borrar: el libro está prestado"

    db.session.delete(libro)
    db.session.commit()
    return True, "Libro borrado"


def listar_libros():
    """Devuelve todos los libros ordenados por título (sin distinguir mayúsculas/minúsculas)."""
    return Libro.query.order_by(func.lower(Libro.titulo)).all()


def listar_disponibles():
    """Devuelve solo los libros disponibles (sin socio asignado) ordenados por título."""
    return (
        Libro.query
        .filter(Libro.socio_id.is_(None))
        .order_by(func.lower(Libro.titulo))
        .all()
    )


def buscar_por_titulo(titulo_parcial: str):
    """Busca libros cuyo título contenga el texto indicado (búsqueda parcial, sin case sensitive)."""
    patron = f"%{titulo_parcial}%"
    return (
        Libro.query
        .filter(func.lower(Libro.titulo).like(func.lower(patron)))
        .all()
    )


def obtener_libro(libro_id: int):
    """Devuelve un libro por id o None si no existe."""
    return Libro.query.get(libro_id)


def crear_libro(titulo, autor, resumen=None, categoria=None, anio=None):
    """Crea y guarda un libro nuevo en la base de datos."""
    libro = Libro(
        titulo=titulo,
        autor=autor,
        resumen=resumen,
        categoria=categoria,
        anio=anio
    )
    db.session.add(libro)
    db.session.commit()
    return libro


def editar_libro(libro_id, titulo=None, autor=None, resumen=None, categoria=None, anio=None):
    """Actualiza campos del libro indicado (solo los que vengan) y lo guarda."""
    libro = Libro.query.get(libro_id)
    if not libro:
        return None

    if titulo is not None:
        libro.titulo = titulo
    if autor is not None:
        libro.autor = autor
    if resumen is not None:
        libro.resumen = resumen
    if categoria is not None:
        libro.categoria = categoria
    if anio is not None:
        libro.anio = anio

    db.session.commit()
    return libro


def obtener_libro_o_404(libro_id: int) -> Libro:
    """Devuelve un libro por id o lanza 404 si no existe."""
    libro = Libro.query.get(libro_id)
    if not libro:
        abort(404)
    return libro
