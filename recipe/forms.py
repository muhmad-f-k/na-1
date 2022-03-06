import wtforms
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, IntegerRangeField, StringField
from wtforms.validators import DataRequired, Length, InputRequired


class CreateRecipeForm(FlaskForm):
    recipeApproach = TextAreaField('Approach', validators=[DataRequired(), Length(min=1, max=10000)])
    recipeVersion = IntegerField('Versjon', validators=[InputRequired()])
    submit = SubmitField('Opprett')
