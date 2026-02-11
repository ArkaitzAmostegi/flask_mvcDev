from flask import Blueprint, render_template

navigation_bp = Blueprint(
    "navigation",
    __name__,
    url_prefix="/"
)  # Blueprint de navegación para páginas públicas (prefijo raíz "/")

@navigation_bp.route("/", methods=["GET"])  # Ruta principal: muestra la página de inicio
def inicio():
    """Renderiza la página de inicio."""
    return render_template("paginas/inicio.html")
