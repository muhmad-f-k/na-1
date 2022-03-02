from flask_wtf import FlaskForm
from  flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Optional


class MakeDinnerForm(FlaskForm):
    mp_name = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    #mp_date = DateField('Dato', validators=[DataRequired()])
    mp_image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Lagre')


class UpdateDinnerForm(FlaskForm):
    mp_id = IntegerField('Middags ID', validators=[DataRequired()])
    mp_name = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    #mp_date = DateField('Dato', validators=[DataRequired()])
    mp_image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Lagre')
