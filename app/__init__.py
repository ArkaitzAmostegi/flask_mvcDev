from flask import Flask
from flask_cors import CORS
from app.extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # carpeta /app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "..", "python.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Blueprints
    from app.controllers.navigation_controller import navigation_bp
    from app.controllers.libros_controller import libros_bp
    from app.controllers.api_controller import api_bp
    from app.controllers.socios_controller import socios_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(navigation_bp)
    app.register_blueprint(libros_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(socios_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        # Importa modelos para que SQLAlchemy configure relaciones
        from app.models.libro import Libro
        from app.models.socio import Socio

        db.create_all()

        # Crear admin si no existe
        if not User.query.filter_by(username="admin").first():
            u = User(username="admin", role="admin")
            u.set_password("1234")
            db.session.add(u)
            db.session.commit()

    return app
