from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BuscarForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Buscar")
