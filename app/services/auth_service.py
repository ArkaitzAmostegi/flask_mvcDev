from app.models.user import User

def autenticar(username: str, password: str):
    """
    Devuelve (user, None) si OK
    Devuelve (None, "mensaje") si error
    """
    user = User.query.filter_by(username=username.strip()).first()
    if not user:
        return None, "Credenciales incorrectas"
    if not user.check_password(password):
        return None, "Credenciales incorrectas"
    return user, None
