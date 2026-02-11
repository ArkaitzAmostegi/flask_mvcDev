from flask import Blueprint, jsonify  # Blueprint para agrupar rutas; jsonify para devolver JSON
from app.services.libros_service import (
    listar_libros, listar_disponibles, buscar_por_titulo  # Lógica de negocio separada (servicios)
)
from app.services.prestamos_service import socios_con_prestamo  # Servicio para socios con préstamos activos


api_bp = Blueprint("api", __name__, url_prefix="/api")  # Prefijo /api para todas las rutas de este blueprint


@api_bp.route("/libros", methods=["GET"])  # Endpoint: lista todos los libros
def api_libros():
    libros = listar_libros()  # Obtiene libros desde el servicio (BD / repositorio)
    return jsonify([l.to_dict() for l in libros])  # Convierte cada libro a dict y lo devuelve en JSON

@api_bp.route("/libros/disponibles", methods=["GET"])  # Endpoint: lista solo libros disponibles
def api_disponibles():
    libros = listar_disponibles()  # Filtra disponibles desde el servicio
    return jsonify([l.to_dict() for l in libros])  # Respuesta JSON con la lista

@api_bp.route("/libros/buscar/<titulo>", methods=["GET"])  # Endpoint: busca por título (parámetro en la URL)
def api_buscar(titulo):
    libros = buscar_por_titulo(titulo)  # Busca coincidencias usando el texto 'titulo'
    return jsonify([l.to_dict() for l in libros])  # Devuelve resultados en JSON

@api_bp.route("/libros/socios/prestamos", methods=["GET"])  # Endpoint: socios que tienen préstamos
def api_socios_prestamos():
    socios = socios_con_prestamo()  # Recupera socios con algún préstamo (según tu lógica)
    return jsonify([s.to_dict() for s in socios])  # Devuelve socios serializados a JSON
