from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DevolucionForm(FlaskForm):
    socio_codigo = StringField("Código de socio", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Devolver")
