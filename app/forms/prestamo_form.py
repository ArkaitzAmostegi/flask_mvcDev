from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PrestamoForm(FlaskForm):
    """Formulario para prestar un libro a un socio mediante su código."""
    socio_codigo = StringField(  # Campo donde se introduce el código del socio
        "Código de socio",
        validators=[
            DataRequired(),  # Obligatorio: no puede ir vacío
            Length(max=20)   # Máximo 20 caracteres
        ]
    )
    submit = SubmitField("Prestar")  # Botón para enviar el préstamo
