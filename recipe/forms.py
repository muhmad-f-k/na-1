from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    recipeApproach = TextAreaField('Approach', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Opprett')
