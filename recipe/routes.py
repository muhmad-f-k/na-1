from flask import Blueprint, render_template
from recipe.forms import CreateRecipeForm, UpdateRecipeForm
from modul import *

recipe = Blueprint('recipe', __name__)


@recipe.route('/create_recipe', methods=['GET', 'POST'])
def createRecipe():
    form = CreateRecipeForm()
    if form.validate():
        dinner_id = 1
        version = 1
        recipe_object = Recipe(approach=form.recipeApproach.data, version=version, dinner_id=dinner_id)
        session.add(recipe_object)
        session.commit()
        session.close()
    return render_template('recipeTemplates/createRecipe.html', form=form)


@recipe.route('/update_recipe', methods=['GET', 'POST'])
def updateRecipe():
    form = UpdateRecipeForm()
    if form.validate():
        dinner_id = 1
        recipe_object = Recipe(approach=form.recipeApproach.data, version=form.recipeVersion.data, dinner_id=dinner_id)
        session.add(recipe_object)
        session.commit()
        session.close()
    return render_template('recipeTemplates/updateRecipe.html', form=form)

