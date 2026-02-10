from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class LibroForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=200)])
    autor = StringField("Autor", validators=[DataRequired(), Length(max=100)])
    resumen = TextAreaField("Resumen", validators=[Optional()])
    categoria = StringField("Categoría", validators=[Optional(), Length(max=80)])
    anio = IntegerField("Año", validators=[Optional(), NumberRange(min=0, max=3000)])
    submit = SubmitField("Guardar")
