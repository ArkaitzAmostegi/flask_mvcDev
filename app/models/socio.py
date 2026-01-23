from app.extensions import db

class Socio(db.Model):
    __tablename__ = "socios"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 1 socio -> 0/1 libro
    libro_prestado = db.relationship(
        "Libro",
        back_populates="socio",
        uselist=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "email": self.email,
            "libro_prestado_id": self.libro_prestado.id if self.libro_prestado else None
        }
