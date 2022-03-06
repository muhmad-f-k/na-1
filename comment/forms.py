from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class postCommentForm(FlaskForm):
    commentText = TextAreaField('Kommentar til middag', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Kommenter')


class editCommentForm(FlaskForm):
    commentText = TextAreaField('Kommentar til middag', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Endre kommentar')
