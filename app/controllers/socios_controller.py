from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from app.forms.socio_form import SocioForm
from app.services.socios_service import listar_socios, crear_socio, editar_socio, obtener_socio
from app.decorators.auth import role_required
from flask import abort
from app.services.socios_service import borrar_socio
from app.forms.socio_buscar_form import SocioBuscarForm
from app.services.socios_service import buscar_socios


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
    if not socio:
        abort(404)

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

@socios_bp.route("/<int:id>/borrar", methods=["POST"])
@role_required("admin")
def borrar(id):
    ok, msg = borrar_socio(id)
    flash(msg, "ok" if ok else "error")
    return redirect(url_for("socios.listar"))

@socios_bp.route("/buscar", methods=["GET","POST"])
@role_required("admin")
def buscar():
    form = SocioBuscarForm()
    socios = []
    if form.validate_on_submit():
        socios = buscar_socios(form.q.data)
    return render_template("paginas/socios/buscar.html", form=form, socios=socios)