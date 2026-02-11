from app.extensions import db

class Libro(db.Model):
    """Modelo ORM de un libro (tabla 'libros')."""
    __tablename__ = "libros"  # Nombre real de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    titulo = db.Column(db.String(200), nullable=False)  # Título obligatorio
    autor = db.Column(db.String(100), nullable=False)  # Autor obligatorio
    resumen = db.Column(db.Text, nullable=True)  # Resumen opcional

    categoria = db.Column(db.String(80), nullable=True)  # Categoría opcional
    anio = db.Column(db.Integer, nullable=True)  # Año opcional

    socio_id = db.Column(db.Integer, db.ForeignKey("socios.id"), nullable=True)  # Socio que lo tiene prestado (si hay)

    socio = db.relationship(
        "Socio",
        back_populates="libro_prestado"  # Relación inversa definida en Socio
    )

    @property
    def disponible(self):
        """Devuelve True si el libro no está prestado (no tiene socio asociado)."""
        return self.socio_id is None
