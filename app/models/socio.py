from app.extensions import db

class Socio(db.Model):
    """Modelo ORM de un socio (tabla 'socios')."""
    __tablename__ = "socios"  # Nombre real de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # Código único y obligatorio
    nombre = db.Column(db.String(120), nullable=False)  # Nombre obligatorio
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único y obligatorio

    libro_prestado = db.relationship(
        "Libro",
        back_populates="socio",  # Relación inversa en Libro.socio
        uselist=False  # Indica relación 1 a 1 (un socio como máximo un libro prestado)
    )

    def to_dict(self):
        """Convierte el socio a diccionario para respuestas JSON."""
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "email": self.email,
            "libro_prestado_id": self.libro_prestado.id if self.libro_prestado else None  # id del libro si tiene
        }
