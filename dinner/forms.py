from flask_wtf import FlaskForm
from  flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional


class MakeDinnerForm(FlaskForm):
    dinnerName = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    mp_day = DateField('Dato', validators=[DataRequired()])
    image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Lagre')
