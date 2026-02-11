from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DevolucionForm(FlaskForm):
    """Formulario para devolver libros indicando el código del socio."""
    socio_codigo = StringField(  # Campo donde se introduce el código del socio
        "Código de socio",
        validators=[
            DataRequired(),   # Obliga a introducir un valor
            Length(max=20)    # Limita el tamaño del código
        ]
    )
    submit = SubmitField("Devolver")  # Botón para enviar la devolución
