from flask import Blueprint, render_template, redirect, url_for, flash

from app.forms.buscar_form import BuscarForm
from app.forms.prestamo_form import PrestamoForm
from app.forms.devolucion_form import DevolucionForm
from app.forms.libro_form import LibroForm

from app.decorators.auth import role_required
from app.decorators.prestamos import validar_prestamo

from app.services.libros_service import (
    listar_libros, listar_disponibles, buscar_por_titulo,
    crear_libro, editar_libro, obtener_libro_o_404, borrar_libro
)

from app.services.prestamos_service import (
    prestar_libro, devolver_por_socio, socios_con_prestamo
)

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")  # Blueprint de libros con prefijo /libros


@libros_bp.route("/", methods=["GET"])  # Ruta: lista todos los libros
def listar():
    """Muestra el listado completo de libros."""
    libros = listar_libros()
    return render_template("paginas/libros/libros.html", libros=libros)


@libros_bp.route("/disponibles", methods=["GET"])  # Ruta: lista solo libros disponibles
def disponibles():
    """Muestra únicamente los libros que están disponibles para préstamo."""
    libros = listar_disponibles()
    return render_template("paginas/libros/libros.html", libros=libros)


@libros_bp.route("/buscar", methods=["GET", "POST"])  # Ruta: formulario de búsqueda y resultados
def buscar():
    """Muestra el formulario de búsqueda y, si se envía, lista resultados por título."""
    form = BuscarForm()
    libros = []
    if form.validate_on_submit():
        libros = buscar_por_titulo(form.titulo.data)
    return render_template("paginas/libros/buscar.html", form=form, libros=libros)


@libros_bp.route("/<int:id>", methods=["GET"])  # Ruta: detalle de un libro
def detalle(id):
    """Muestra el detalle de un libro y el formulario para poder prestarlo."""
    libro = obtener_libro_o_404(id)
    form = PrestamoForm()
    return render_template("paginas/libros/detalle.html", libro=libro, form=form)


@libros_bp.route("/<int:id>/prestar", methods=["POST"])  # Ruta: realiza el préstamo de un libro
@validar_prestamo()  # Valida reglas del préstamo (por ejemplo: libro disponible, socio válido, etc.)
@role_required("admin")  # Solo admin puede prestar
def prestar(id):
    """Procesa el préstamo del libro indicado para el socio del formulario."""
    form = PrestamoForm()
    if form.validate_on_submit():
        ok, msg = prestar_libro(id, form.socio_codigo.data)
        flash(msg, "ok" if ok else "error")
    return redirect(url_for("libros.detalle", id=id))


@libros_bp.route("/<int:id>/editar", methods=["GET", "POST"])  # Ruta: editar un libro
@role_required("admin")  # Solo admin puede editar
def editar(id):
    """Muestra el formulario de edición y guarda los cambios del libro."""
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


@libros_bp.route("/crear", methods=["GET", "POST"])  # Ruta: crear un libro
@role_required("admin")  # Solo admin puede crear
def crear():
    """Muestra el formulario de alta y crea un libro nuevo."""
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


@libros_bp.route("/devolver", methods=["GET", "POST"])  # Ruta: devolución por código de socio
@role_required("admin")  # Solo admin puede gestionar devoluciones
def devolver():
    """Permite devolver libros indicando el código del socio (devuelve sus préstamos según tu lógica)."""
    form = DevolucionForm()
    if form.validate_on_submit():
        ok, msg = devolver_por_socio(form.socio_codigo.data)
        flash(msg, "ok" if ok else "error")
        return redirect(url_for("libros.devolver"))
    return render_template("paginas/libros/devolver.html", form=form)


@libros_bp.route("/socios/prestamos", methods=["GET"])  # Ruta: listado de socios con préstamo
@role_required("admin")  # Solo admin puede ver este listado
def prestamos():
    """Muestra los socios que tienen préstamos activos."""
    socios = socios_con_prestamo()
    return render_template("paginas/socios/prestamos.html", socios=socios)


@libros_bp.route("/grid", methods=["GET"])  # Ruta: vista alternativa en grid
def grid():
    """Muestra los libros en formato rejilla (grid)."""
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)


@libros_bp.route("/<int:id>/borrar", methods=["POST"])  # Ruta: borra un libro
@role_required("admin")  # Solo admin puede borrar
def borrar(id):
    """Elimina un libro por id y vuelve al listado."""
    ok, msg = borrar_libro(id)
    flash(msg, "ok" if ok else "error")
    return redirect(url_for("libros.listar"))
