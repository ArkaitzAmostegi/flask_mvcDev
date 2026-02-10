# app/seed.py
import random
from app.extensions import db
from app.models.libro import Libro
from app.models.socio import Socio

def seed_data():
    """
    Crea socios y libros de ejemplo.
    - Algunos socios con libro prestado (máx 1 por socio)
    - Otros socios sin préstamo
    - Algunos libros disponibles
    """
    # Si ya hay datos, no duplicar (puedes borrar a mano la BD si quieres reseed)
    if Socio.query.first() or Libro.query.first():
        return False, "Ya existen datos. Borra python.db si quieres resembrar."

    socios = [
        Socio(codigo="S001", nombre="Ane Garcia", email="ane@demo.com"),
        Socio(codigo="S002", nombre="Iker Lopez", email="iker@demo.com"),
        Socio(codigo="S003", nombre="Maite Ruiz", email="maite@demo.com"),
        Socio(codigo="S004", nombre="Jon Perez", email="jon@demo.com"),
        Socio(codigo="S005", nombre="Nerea Soto", email="nerea@demo.com"),
        Socio(codigo="S006", nombre="Unai Diaz", email="unai@demo.com"),
        Socio(codigo="S007", nombre="Leire Martin", email="leire@demo.com"),
        Socio(codigo="S008", nombre="Aitor Alonso", email="aitor@demo.com"),
    ]
    db.session.add_all(socios)
    db.session.flush()  # para tener IDs sin commit aún

    libros = [
        Libro(titulo="Clean Code", autor="Robert C. Martin", categoria="Programación", anio=2008,
              resumen="Buenas prácticas para escribir código limpio."),
        Libro(titulo="The Pragmatic Programmer", autor="Andrew Hunt", categoria="Programación", anio=1999,
              resumen="Consejos prácticos para desarrolladores."),
        Libro(titulo="Design Patterns", autor="Gamma et al.", categoria="Arquitectura", anio=1994,
              resumen="Patrones de diseño clásicos."),
        Libro(titulo="Fluent Python", autor="Luciano Ramalho", categoria="Python", anio=2015,
              resumen="Python avanzado y buenas prácticas."),
        Libro(titulo="Python Crash Course", autor="Eric Matthes", categoria="Python", anio=2016,
              resumen="Introducción práctica a Python."),
        Libro(titulo="Automate the Boring Stuff", autor="Al Sweigart", categoria="Python", anio=2015,
              resumen="Automatización con Python."),
        Libro(titulo="Eloquent JavaScript", autor="Marijn Haverbeke", categoria="JavaScript", anio=2018,
              resumen="JavaScript moderno en profundidad."),
        Libro(titulo="You Don't Know JS", autor="Kyle Simpson", categoria="JavaScript", anio=2015,
              resumen="Serie para entender JS a fondo."),
        Libro(titulo="Refactoring", autor="Martin Fowler", categoria="Programación", anio=1999,
              resumen="Mejorar diseño de código existente."),
        Libro(titulo="Domain-Driven Design", autor="Eric Evans", categoria="Arquitectura", anio=2003,
              resumen="Modelado de dominio y diseño."),
        Libro(titulo="Introduction to Algorithms", autor="Cormen et al.", categoria="Algoritmos", anio=2009,
              resumen="Algoritmos y estructuras de datos."),
        Libro(titulo="SQL Cookbook", autor="Anthony Molinaro", categoria="Bases de datos", anio=2005,
              resumen="Recetas SQL para casos comunes."),
    ]
    db.session.add_all(libros)
    db.session.flush()

    # Asignar préstamos: 3 socios con libro, 5 socios sin libro
    socios_con_prestamo = [socios[0], socios[2], socios[5]]  # S001, S003, S006
    libros_a_prestar = [libros[0], libros[3], libros[7]]     # 3 libros

    for socio, libro in zip(socios_con_prestamo, libros_a_prestar):
        libro.socio_id = socio.id  # préstamo

    db.session.commit()
    return True, "Seed completado: socios/libros creados con préstamos y disponibles."
