from flask import Blueprint, render_template
from recipe.forms import CreateRecipeForm
from modul import *

recipe = Blueprint('recipe', __name__)


@recipe.route('/create_recipe', methods=['GET', 'POST'])
def createRecipe():
    form = CreateRecipeForm()
    dinner_id = 1
    if form.validate_on_submit():
        recipe = Recipe(approach=form.recipeApproach, version=form.recipeVersion, dinner_id=dinner_id)
        session.add(recipe)
        session.commit()
    return render_template('recipe.html', form=form)
