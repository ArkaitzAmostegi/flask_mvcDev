from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """Modelo de usuario para autenticación (compatible con Flask-Login)."""
    __tablename__ = "users_auth"  # Tabla donde se guardan los usuarios

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    username = db.Column(db.String(50), unique=True, nullable=False)  # Usuario único y obligatorio
    password_hash = db.Column(db.String(255), nullable=False)  # Hash de la contraseña 
    role = db.Column(db.String(20), nullable=False, default="admin")  # Rol para controlar permisos

    def set_password(self, password: str):
        """Guarda la contraseña de forma segura (hash) en password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Comprueba si la contraseña indicada coincide con el hash guardado."""
        return check_password_hash(self.password_hash, password)
