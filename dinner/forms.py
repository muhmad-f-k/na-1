from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    dinnerName = StringField('Username',
                             validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Lagre')
