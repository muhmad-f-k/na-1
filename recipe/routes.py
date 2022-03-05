from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from recipe.forms import recipeform

recipe = Blueprint('recipe', __name__)


@recipe.route('/recipe')
def index():
    form = recipeform()
    return render_template('recipe.html', form=form)
