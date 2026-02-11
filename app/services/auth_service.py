from app.models.user import User

def autenticar(username: str, password: str):
    """Valida credenciales y devuelve (user, None) si son correctas o (None, 'mensaje') si fallan."""
    user = User.query.filter_by(username=username.strip()).first()  # Busca el usuario por username
    if not user:
        return None, "Credenciales incorrectas"  # No existe usuario con ese nombre
    if not user.check_password(password):
        return None, "Credenciales incorrectas"  # La contraseña no coincide con el hash guardado
    return user, None  # Login correcto
