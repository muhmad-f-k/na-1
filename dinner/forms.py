from flask_wtf import FlaskForm
from  flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Optional


class MakeDinnerForm(FlaskForm):
    mp_dinner_title = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    #mp_date = DateField('Dato', validators=[DataRequired()])
    mp_dinner_image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Lagre')


class UpdateDinnerForm(FlaskForm):
    mp_dinner_id = IntegerField('Middags ID', validators=[DataRequired()])
    mp_dinner_title = StringField('Navn',
                             validators=[DataRequired(), Length(min=2, max=20)])
    #mp_date = DateField('Dato', validators=[DataRequired()])
    mp_dinner_image = FileField('Bilde av middag',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Oppdater')


class DeleteDinnerForm(FlaskForm):
    mp_dinner_id = IntegerField('Middags ID', validators=[DataRequired()])
    submit = SubmitField('Slett')