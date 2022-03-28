from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import *
from sqlalchemy import desc


recipe_route = Blueprint('recipe_route', __name__)


@recipe_route.route('/create_recipe/<dinner_id>')
def createRecipe(dinner_id):
    return render_template('createrecipe.html', dinner_id=dinner_id)


@recipe_route.route('/create_recipe/<dinner_id>', methods=['POST'])
def createRecipe_post(dinner_id):
    highest_existing_version = session.query(Recipe.version).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version).limit(1))
    if highest_existing_version:
        recipe_version = highest_existing_version + 1

    else:
        recipe_version = 1

    approach = str(request.form.get("textareaApproach"))
    recipe_object = Recipe(
        approach=approach, version=recipe_version, dinner_id=dinner_id)
    session.add(recipe_object)
    session.commit()
    return redirect(url_for("recipe_route.add_ingredients", dinner_id=dinner_id))


@recipe_route.route("/add_ingredients")
def add_ingredients():
    recipe_id = 1
    measurements = session.query(Measurement).all()
    session.close()
    ingredients_recipe = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()
    session.close()
    amounts_recipe = session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()
    session.close()
    measurements_recipe = session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()
    session.close()
    return render_template("addrecipeIngredient.html", measurements=measurements, len=len(ingredients_recipe),
                           ingredients=ingredients_recipe, amount=amounts_recipe,
                           measurements_recipe=measurements_recipe)


@recipe_route.route('/add_ingredients', methods=['POST'])
def add_ingredients_post():
    ingredient = request.form.get("ingredient")
    amount = request.form.get("amount")
    unit = request.form.get("unit")

    shopping_list = "13"
    recipe = "apro"
    ingredient_check = session.query(Ingredient).filter(
        Ingredient.name == ingredient).first()
    session.close()
    amount_check = session.query(Amount).filter(
        Amount.amount == amount).first()
    session.close()
    if ingredient_check and amount_check:
        print("det finnes ingrediens, og det finnes amount i generell tabell")
    if ingredient_check and not amount_check:
        print("det finnes ingrediens, men ikke amount")
        new_amount = Amount(amount=amount)
        session.add(new_amount)
        session.commit()
        session.close()
    if not ingredient_check and amount_check:
        print("det finnes ikke ingrediens, men det finnes amount")
        new_ingredient = Ingredient(name=ingredient)
        session.add(new_ingredient)
        session.commit()
        session.close()
    if not ingredient_check and not amount_check:
        print("ingen av delene finnes")
        new_amount = Amount(amount=amount)
        new_ingredient = Ingredient(name=ingredient)
        session.add_all([new_ingredient, new_amount])
        session.commit()
        session.close()

    ingredients = session.query(Ingredient).filter(
        Ingredient.name == ingredient).first()
    session.close()
    amounts = session.query(Amount).filter(Amount.amount == amount).first()
    session.close()
    shopping_lists = session.query(Shopping_list).filter(
        Shopping_list.price == shopping_list).first()
    session.close()
    recipes = session.query(Recipe).filter(Recipe.approach == recipe).first()
    session.close()
    units = session.query(Measurement).filter(Measurement.name == unit).first()
    session.close()
    final = Recipe_ingredient_helper(ingredient=ingredients, recipe=recipes, amount=amounts,
                                     shopping_list=shopping_lists,
                                     measurement=units)
    session.add(final)
    session.commit()
    session.close()

    return redirect(url_for("recipe_route.add_ingredients"))


@recipe_route.route('/remove_ingredient/<ingredient_name>', methods=['POST'])
def remove_ingredient(ingredient_name):
    recipe_id = 1
    delete_ingredient = session.query(Ingredient).filter(
        Ingredient.name == ingredient_name).first()
    session.close()
    delete_data = session.query(Recipe_ingredient_helper).filter(
        Recipe_ingredient_helper.ingredient_id == delete_ingredient.id, Recipe_ingredient_helper.recipe_id == recipe_id).first()
    session.delete(delete_data)
    session.commit()
    session.close()

    return redirect(url_for("recipe_route.add_ingredients"))


@recipe_route.route('/update_recipe')
def updateRecipe():
    return render_template('updaterecipe.html')


@recipe_route.route('/update_recipe', methods=['POST'])
def updateRecipe_post():
    dinner_id = 1
    version = (session.query(Recipe.version) + 1)
    session.close()
    approach = str(request.form.get("textareaApproach"))
    recipe_object = Recipe(
        approach=approach, version=version, dinner_id=dinner_id)
    session.add(recipe_object)
    session.commit()
    session.close()
    return redirect(url_for("recipe_route.add_ingredients"))
