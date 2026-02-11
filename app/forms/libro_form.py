from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class LibroForm(FlaskForm):
    """Formulario para crear o editar un libro."""
    titulo = StringField(  # Título obligatorio (máx. 200)
        "Título",
        validators=[DataRequired(), Length(max=200)]
    )
    autor = StringField(  # Autor obligatorio (máx. 100)
        "Autor",
        validators=[DataRequired(), Length(max=100)]
    )
    resumen = TextAreaField(  # Resumen opcional (texto largo)
        "Resumen",
        validators=[Optional()]
    )
    categoria = StringField(  # Categoría opcional (máx. 80)
        "Categoría",
        validators=[Optional(), Length(max=80)]
    )
    anio = IntegerField(  # Año opcional, pero si se rellena debe estar dentro del rango
        "Año",
        validators=[Optional(), NumberRange(min=0, max=3000)]
    )
    submit = SubmitField("Guardar")  # Botón de enviar (crear/editar)
