from flask import Blueprint, jsonify
from app.services.libros_service import (
    listar_libros, listar_disponibles, buscar_por_titulo, socios_con_prestamo
)

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/libros", methods=["GET"])
def api_libros():
    libros = listar_libros()
    return jsonify([l.to_dict() for l in libros])

@api_bp.route("/libros/disponibles", methods=["GET"])
def api_disponibles():
    libros = listar_disponibles()
    return jsonify([l.to_dict() for l in libros])

@api_bp.route("/libros/buscar/<titulo>", methods=["GET"])
def api_buscar(titulo):
    libros = buscar_por_titulo(titulo)
    return jsonify([l.to_dict() for l in libros])

@api_bp.route("/libros/socios/prestamos", methods=["GET"])
def api_socios_prestamos():
    socios = socios_con_prestamo()
    return jsonify([s.to_dict() for s in socios])
