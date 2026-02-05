from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from app.forms.socio_form import SocioForm
from app.services.socios_service import listar_socios, crear_socio, editar_socio, obtener_socio
from app.decorators.auth import role_required


socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

@socios_bp.route("/")
@role_required("admin")
def listar():
    socios = listar_socios()
    return render_template("paginas/socios/socios.html", socios=socios)

@socios_bp.route("/crear", methods=["GET", "POST"])
@role_required("admin")
def crear():
    form = SocioForm()
    if form.validate_on_submit():
        try:
            crear_socio(
                codigo=form.codigo.data.strip(),
                nombre=form.nombre.data.strip(),
                email=form.email.data.strip()
            )
            flash("Socio creado", "ok")
            return redirect(url_for("socios.listar"))
        except IntegrityError:
            flash("Código o email ya existen", "error")
    return render_template("paginas/socios/socio_form.html", form=form, modo="crear")

@socios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@role_required("admin")
def editar(id):
    socio = obtener_socio(id)
    if socio:
        form = SocioForm(obj=socio)

        if form.validate_on_submit():
            try:
                editar_socio(
                    socio_id=id,
                    codigo=form.codigo.data.strip(),
                    nombre=form.nombre.data.strip(),
                    email=form.email.data.strip()
                )
                flash("Socio actualizado", "ok")
                return redirect(url_for("socios.listar"))
            except IntegrityError:
                flash("Código o email ya existen", "error")

        return render_template("paginas/socios/socio_form.html", form=form, modo="editar", socio=socio)
