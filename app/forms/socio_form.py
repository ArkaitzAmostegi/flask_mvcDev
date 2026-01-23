from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class SocioForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired(), Length(max=20)])
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField("Guardar")
