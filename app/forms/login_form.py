from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión."""
    username = StringField(  # Usuario obligatorio (máx. 50)
        "Usuario",
        validators=[DataRequired(), Length(max=50)]
    )
    password = PasswordField(  # Contraseña obligatoria (entre 4 y 128)
        "Password",
        validators=[DataRequired(), Length(min=4, max=128)]
    )
    submit = SubmitField("Entrar")  # Botón para enviar el login
