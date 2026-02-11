# app/forms/socio_buscar_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SocioBuscarForm(FlaskForm):
    """Formulario para buscar socios por nombre o email."""
    q = StringField(  # Texto de búsqueda (nombre o email)
        "Buscar (nombre o email)",
        validators=[
            DataRequired(),  # Obligatorio: debe introducirse algo
            Length(max=120)  # Límite para evitar textos demasiado largos
        ]
    )
    submit = SubmitField("Buscar")  # Botón para lanzar la búsqueda
