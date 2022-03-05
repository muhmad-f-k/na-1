from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import *


class RegistrationForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Length(min=4, max=20)])
    first_name = StringField('fornavn  ', [DataRequired(), Length(min=1, max=30)])
    surname = StringField('Etternavn', [DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Lagre')
