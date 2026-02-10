from flask import Blueprint, render_template, redirect, url_for, flash

from app.forms.buscar_form import BuscarForm
from app.forms.prestamo_form import PrestamoForm
from app.forms.devolucion_form import DevolucionForm
from app.forms.libro_form import LibroForm

from app.decorators.auth import role_required
from app.decorators.prestamos import validar_prestamo

from app.services.libros_service import (
    listar_libros, listar_disponibles, buscar_por_titulo,
    crear_libro, editar_libro, obtener_libro_o_404
)

from app.services.prestamos_service import (
    prestar_libro, devolver_por_socio, socios_con_prestamo
)

from app.services.libros_service import borrar_libro

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")


@libros_bp.route("/")
def listar():
    libros = listar_libros()
    return render_template("paginas/libros/libros.html", libros=libros)


@libros_bp.route("/disponibles")
def disponibles():
    libros = listar_disponibles()
    return render_template("paginas/libros/libros.html", libros=libros)


@libros_bp.route("/buscar", methods=["GET", "POST"])
def buscar():
    form = BuscarForm()
    libros = []
    if form.validate_on_submit():
        libros = buscar_por_titulo(form.titulo.data)
    return render_template("paginas/libros/buscar.html", form=form, libros=libros)


# DETALLE (ver + form de préstamo)
@libros_bp.route("/<int:id>", methods=["GET"])
def detalle(id):
    libro = obtener_libro_o_404(id)
    form = PrestamoForm()
    return render_template("paginas/libros/detalle.html", libro=libro, form=form)


# PRESTAR (POST)
@libros_bp.route("/<int:id>/prestar", methods=["POST"])
@validar_prestamo()
@role_required("admin")
def prestar(id):
    form = PrestamoForm()
    if form.validate_on_submit():
        ok, msg = prestar_libro(id, form.socio_codigo.data)
        flash(msg, "ok" if ok else "error")
    return redirect(url_for("libros.detalle", id=id))


# EDITAR (GET+POST) EN RUTA DISTINTA
@libros_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@role_required("admin")
def editar(id):
    libro = obtener_libro_o_404(id)
    form = LibroForm(obj=libro)

    if form.validate_on_submit():
        editar_libro(
            libro_id=id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data,
            categoria=form.categoria.data,
            anio=form.anio.data
        )
        flash("Libro actualizado", "ok")
        return redirect(url_for("libros.detalle", id=id))

    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)


@libros_bp.route("/crear", methods=["GET", "POST"])
@role_required("admin")
def crear():
    form = LibroForm()
    if form.validate_on_submit():
        crear_libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data,
            categoria=form.categoria.data,
            anio=form.anio.data
        )
        flash("Libro creado", "ok")
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_crear.html", form=form)



@libros_bp.route("/devolver", methods=["GET", "POST"])
@role_required("admin")
def devolver():
    form = DevolucionForm()
    if form.validate_on_submit():
        ok, msg = devolver_por_socio(form.socio_codigo.data)
        flash(msg, "ok" if ok else "error")
        return redirect(url_for("libros.devolver"))
    return render_template("paginas/libros/devolver.html", form=form)


@libros_bp.route("/socios/prestamos")
@role_required("admin")
def prestamos():
    socios = socios_con_prestamo()
    return render_template("paginas/socios/prestamos.html", socios=socios)


@libros_bp.route("/grid")
def grid():
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)


@libros_bp.route("/<int:id>/borrar", methods=["POST"])
@role_required("admin")
def borrar(id):
    ok, msg = borrar_libro(id)
    flash(msg, "ok" if ok else "error")
    return redirect(url_for("libros.listar"))