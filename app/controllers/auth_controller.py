from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.forms.login_form import LoginForm
from app.services.auth_service import autenticar

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")  # Agrupa rutas de autenticación bajo /auth

@auth_bp.route("/login", methods=["GET", "POST"])  # Muestra el login (GET) y procesa credenciales (POST)
def login():
    form = LoginForm()  # Formulario de acceso (WTForms)
    if form.validate_on_submit():  # Solo si es POST y el formulario es válido (incluye CSRF)
        user, error = autenticar(form.username.data, form.password.data)  # Verifica usuario/contraseña
        if user:
            login_user(user)  # Inicia sesión con Flask-Login
            next_url = request.args.get("next")  # Redirección a la página originalmente solicitada (si existe)
            return redirect(next_url or url_for("navigation.inicio"))  # Si no hay next, vuelve a inicio
        flash(error, "error")  # Si falla, muestra el error en pantalla
    return render_template("paginas/auth/login.html", form=form)  # Renderiza la vista del login

@auth_bp.route("/logout")  # Cierra sesión
@login_required  # Protege la ruta: requiere estar logueado
def logout():
    logout_user()  # Termina la sesión del usuario
    flash("Sesión cerrada", "ok")  # Mensaje de confirmación
    return redirect(url_for("navigation.inicio"))  # Vuelve a inicio
