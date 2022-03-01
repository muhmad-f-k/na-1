from flask_wtf import FlaskForm
from  flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    dinnerName = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png']), FileRequired()])
    submit = SubmitField('Lagre')
