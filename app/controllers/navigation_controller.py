from flask import Blueprint, render_template

navigation_bp = Blueprint(
    "navigation",
    __name__,
    url_prefix="/"
)

@navigation_bp.route("/")
def inicio():
    return render_template("paginas/inicio.html")

