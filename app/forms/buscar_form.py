from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BuscarForm(FlaskForm):
    """Formulario para buscar libros por título."""
    titulo = StringField(  # Campo de texto donde el usuario escribe el título a buscar
        "Título",
        validators=[
            DataRequired(),     # Obliga a rellenar el campo (no vacío)
            Length(max=200)     # Limita la longitud para evitar entradas demasiado largas
        ]
    )
    submit = SubmitField("Buscar")  # Botón para enviar el formulario
