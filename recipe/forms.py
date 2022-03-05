from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length


class CreateRecipeForm(FlaskForm):
    recipeApproach = TextAreaField('Approach', validators=[DataRequired(), Length(min=1, max=1000)])
    recipeVersion = IntegerField('Versjon', validators=[DataRequired(), Length(min=1, max=10000)])
    submit = SubmitField('Opprett')