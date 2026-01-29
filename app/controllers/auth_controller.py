from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.forms.login_form import LoginForm
from app.services.auth_service import autenticar

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, error = autenticar(form.username.data, form.password.data)
        if user:
            login_user(user)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("navigation.inicio"))
        flash(error, "error")
    return render_template("paginas/auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "ok")
    return redirect(url_for("navigation.inicio"))
