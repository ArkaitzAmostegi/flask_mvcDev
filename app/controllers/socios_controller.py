from flask import Blueprint, render_template, redirect, url_for, flash, abort
from sqlalchemy.exc import IntegrityError

from app.forms.socio_form import SocioForm
from app.forms.socio_buscar_form import SocioBuscarForm

from app.decorators.auth import role_required

from app.services.socios_service import (
    listar_socios, crear_socio, editar_socio, obtener_socio, borrar_socio, buscar_socios
)

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")  # Blueprint de socios con prefijo /socios


@socios_bp.route("/", methods=["GET"])  # Ruta: lista de socios
@role_required("admin")  # Solo admin puede acceder
def listar():
    """Muestra el listado de socios."""
    socios = listar_socios()
    return render_template("paginas/socios/socios.html", socios=socios)


@socios_bp.route("/crear", methods=["GET", "POST"])  # Ruta: crear socio
@role_required("admin")  # Solo admin puede crear
def crear():
    """Muestra el formulario y crea un socio nuevo (controla duplicados de código/email)."""
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


@socios_bp.route("/<int:id>/editar", methods=["GET", "POST"])  # Ruta: editar socio
@role_required("admin")  # Solo admin puede editar
def editar(id):
    """Muestra el formulario de edición y guarda cambios del socio (404 si no existe)."""
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


@socios_bp.route("/<int:id>/borrar", methods=["POST"])  # Ruta: borrar socio
@role_required("admin")  # Solo admin puede borrar
def borrar(id):
    """Elimina un socio por id y vuelve al listado."""
    ok, msg = borrar_socio(id)
    flash(msg, "ok" if ok else "error")
    return redirect(url_for("socios.listar"))


@socios_bp.route("/buscar", methods=["GET", "POST"])  # Ruta: buscar socios
@role_required("admin")  # Solo admin puede buscar
def buscar():
    """Muestra el buscador y lista socios que coinciden con la consulta."""
    form = SocioBuscarForm()
    socios = []
    if form.validate_on_submit():
        socios = buscar_socios(form.q.data)
    return render_template("paginas/socios/buscar.html", form=form, socios=socios)
