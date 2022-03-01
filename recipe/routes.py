from flask import Blueprint, render_template
from recipe.forms import RegistrationForm

recipe = Blueprint('recipe', __name__)


@recipe.route('/recipe')
def index():
    form = RegistrationForm()
    return render_template('recipe.html', form=form)