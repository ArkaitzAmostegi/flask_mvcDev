from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class SocioForm(FlaskForm):
    """Formulario para crear o editar un socio."""
    codigo = StringField(  # Código obligatorio (máx. 20)
        "Código",
        validators=[DataRequired(), Length(max=20)]
    )
    nombre = StringField(  # Nombre obligatorio (máx. 120)
        "Nombre",
        validators=[DataRequired(), Length(max=120)]
    )
    email = StringField(  # Email obligatorio, debe tener formato válido (máx. 120)
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    submit = SubmitField("Guardar")  # Botón para guardar cambios
