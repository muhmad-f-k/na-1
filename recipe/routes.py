from flask import Blueprint, render_template
from recipe.forms import CreateRecipeForm
from modul import *

recipe = Blueprint('recipe', __name__)


@recipe.route('/create_recipe', methods=['GET', 'POST'])
def createRecipe():
    form = CreateRecipeForm()
    if form.validate():
        print(form.errors)
        dinner_id = 1
        recipepanne = Recipe(approach=form.recipeApproach.data, version=form.recipeVersion.data, dinner_id=dinner_id)
        session.add(recipepanne)
        session.commit()
    return render_template('recipe.html', form=form)
