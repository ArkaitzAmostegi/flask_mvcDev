# app/forms/socio_buscar_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SocioBuscarForm(FlaskForm):
    q = StringField("Buscar (nombre o email)", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Buscar")
