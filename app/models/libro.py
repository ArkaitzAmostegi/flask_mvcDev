from app.extensions import db

class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    genero = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    resumen = db.Column(db.Text, nullable=True)

    categoria = db.Column(db.String(80), nullable=True)
    anio = db.Column(db.Integer, nullable=True)

    socio_id = db.Column(db.Integer, db.ForeignKey("socios.id"), nullable=True)

    socio = db.relationship("Socio", back_populates="libro_prestado")

    @property
    def disponible(self):
        return self.socio_id is None

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "autor": self.autor,
            "resumen": self.resumen,
            "categoria": self.categoria,
            "anio": self.anio,
            "socio_id": self.socio_id,
            "disponible": self.disponible,
        }
