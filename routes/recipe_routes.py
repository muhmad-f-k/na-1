from base64 import b64encode

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user

from queries import recipe_queries as rq
from db.modul import *
from sqlalchemy import desc

recipe_route = Blueprint('recipe_route', __name__)


@recipe_route.route('/create_recipe/<dinner_id>')
def createRecipe(dinner_id):
    return render_template('dinners/create_recipe.html', dinner_id=dinner_id)


@recipe_route.route('/create_recipe/<dinner_id>', methods=['POST'])
def createRecipe_post(dinner_id):
    highest_existing_version = session.query(Recipe.version).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    if highest_existing_version:
        recipe_version = int(highest_existing_version) + 1

    else:
        recipe_version = 1

    approach = str(request.form.get("dinner-approach"))
    portions = int(request.form.get("portions"))
    recipe_object = Recipe(
        approach=approach, version=recipe_version, portions=portions, dinner_id=dinner_id)
    session.add(recipe_object)
    session.commit()
    return redirect(url_for("recipe_route.add_ingredients", recipe_id=recipe_object.id, dinner_id=dinner_id))


@recipe_route.route("/add_ingredients/<recipe_id>")
def add_ingredients(recipe_id):
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
    return render_template("dinners/create_ingredients.html", measurements=measurements, len=len(ingredients_recipe),
                           ingredients=ingredients_recipe, amount=amounts_recipe,
                           measurements_recipe=measurements_recipe, recipe_id=recipe_id)


@recipe_route.route('/add_ingredients/<recipe_id>', methods=['POST'])
def add_ingredients_post(recipe_id):
    if "ingredient" in request.form:
        ingredient = request.form.get("ingredient")
        amount = request.form.get("amount")
        unit = request.form.get("unit")

        recipe = session.query(Recipe).filter(
            Recipe.id == recipe_id).first()
        ingredient_check = session.query(Ingredient).filter(
            Ingredient.name == ingredient).first()
        amount_check = session.query(Amount).filter(
            Amount.amount == amount).first()
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

        ingredients = session.query(Ingredient).filter(
            Ingredient.name == ingredient).first()
        amounts = session.query(Amount).filter(Amount.amount == amount).first()
        units = session.query(Measurement).filter(Measurement.name == unit).first()
        session.close()
        final = Recipe_ingredient_helper(ingredient=ingredients, recipe=recipe, amount=amounts, measurement=units)
        session.add(final)
        session.commit()
    if "delIngredient" in request.form:
        recipe_id = request.form.get("recipe_id")
        print(recipe_id)
        ingredient_name = request.form.get("ingredient_name")
        print(ingredient_name)
        delete_ingredient = session.query(Ingredient).filter(
            Ingredient.name == request.form.get("ingredient_name")).first()
        session.close()
        delete_data = session.query(Recipe_ingredient_helper).filter(
            Recipe_ingredient_helper.ingredient_id == delete_ingredient.id,
            Recipe_ingredient_helper.recipe_id == recipe_id).first()
        session.delete(delete_data)
        session.commit()
        session.close()
    return redirect(url_for("recipe_route.add_ingredients", recipe_id=recipe_id))


@recipe_route.route('/show_changes_recipe/<dinner_id>')
def show_changes_recipe(dinner_id):
    dinner = session.query(Dinner).filter(Dinner.id == dinner_id).first()
    # nåværende
    recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).all()
    current_version_id = recipe_version[0].id

    recipe = session.query(Recipe).filter(Recipe.id == current_version_id).first()
    ingredients_recipe = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()
    session.close()
    amounts_recipe = session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()
    session.close()
    measurements_recipe = session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()
    session.close()

    # tidligere
    ingredients_recipe_prev = ""
    amounts_recipe_prev = ""
    measurements_recipe_prev = ""
    recipe_prev = ""
    len_prev = 0
    ingredient_status = ""
    approach_status = ""
    if len(recipe_version) < 2:
        print('Det finnes kun en versjon av denne')
        approach_status = "Det finnes ingen tidligere versjoner av denne oppskriften"
        ingredient_status = "Det finnes ingen tidligere versjoner av denne oppskriften"
    elif len(recipe_version) == 2 or len(recipe_version) > 2:
        previous_version_id = recipe_version[1].id
        print('det finnes flere versjoner')
        recipe_prev = session.query(Recipe).filter(
            Recipe.id == previous_version_id).first()
        ingredients_recipe_prev = session.query(Ingredient.name).join(
            Recipe_ingredient_helper).join(Recipe).filter(
            Recipe.id == previous_version_id).all()
        session.close()
        amounts_recipe_prev = session.query(Amount.amount).join(
            Recipe_ingredient_helper).join(Recipe).filter(
            Recipe.id == previous_version_id).all()
        session.close()
        measurements_recipe_prev = session.query(Measurement.name).join(
            Recipe_ingredient_helper).join(Recipe).filter(
            Recipe.id == previous_version_id).all()
        session.close()

        len_prev = len(ingredients_recipe_prev)

    return render_template("dinners/changed_recipe.html",
                           dinner=dinner,
                           recipe=recipe,
                           len=len(ingredients_recipe),
                           ingredients=ingredients_recipe,
                           amounts=amounts_recipe,
                           measurements=measurements_recipe,
                           ingredients_prev=ingredients_recipe_prev,
                           amounts_prev=amounts_recipe_prev,
                           measurements_prev=measurements_recipe_prev,
                           len_prev=len_prev,
                           recipe_prev=recipe_prev,
                           status_ingredient=ingredient_status,
                           status_approach=approach_status)


@recipe_route.route('/change_Recipe/<dinner_id>/<group_id>')
def change_recipe(dinner_id, group_id):
    current_user_role = session.query(User_group_role).filter(
        User_group_role.user_id == current_user.id,
        User_group_role.group_id == group_id).first()

    dinner = session.query(Dinner).filter(Dinner.id == dinner_id).first()
    # nåværende
    recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).all()
    current_version_id = recipe_version[0].id

    recipe = session.query(Recipe).filter(Recipe.id == current_version_id).first()

    ingredients_recipe = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()

    measurement_recipe_helper = session.query(Measurement.name).join(Recipe_ingredient_helper).join(Recipe).filter(
        Recipe_ingredient_helper.recipe_id == current_version_id
    ).all()

    amounts_recipe = session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()

    measurements_recipe = session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(
        Recipe.id == current_version_id).all()

    measurements = session.query(Measurement).all()

    return render_template("dinners/change_recipe.html",
                           dinner=dinner,
                           recipe=recipe,
                           len=len(ingredients_recipe),
                           ingredients=ingredients_recipe,
                           measurement_recipe_helper=measurement_recipe_helper,
                           amounts=amounts_recipe,
                           measurements=measurements,
                           measurements_recipe=measurements_recipe,
                           current_user_role=current_user_role,
                           dinner_id=dinner_id,
                           group_id=group_id
                           )


@recipe_route.route('/change_Recipe/<dinner_id>/<group_id>', methods=['POST'])
def change_recipe_post(dinner_id, group_id):
    highest_recipe_version = rq.get_highest_recipe_version_with_dinner_id(dinner_id)
    approach = request.form.get("textareaApproach")
    if "textareaApproach" in request.form:
        rq.add_new_version_to_recipe(approach, dinner_id)
        new_highest_version = rq.get_highest_recipe_version_with_dinner_id(dinner_id)
        original_ingredients = rq.get_ingredients_with_highest_recipe_version(highest_recipe_version)
        original_amounts = rq.get_amounts_with_highest_recipe_version(highest_recipe_version)
        original_measurements = rq.get_measurements_with_highest_recipe_version(highest_recipe_version)

        for i in range(0, len(original_ingredients)):
            helper_object = Recipe_ingredient_helper(
                measurement_id=original_measurements[i].id,
                amount_id=original_amounts[i].id,
                ingredient_id=original_ingredients[i].id,
                recipe_id=new_highest_version.id)
            session.add(helper_object)
            session.commit()

    if "ingredient" in request.form:
        get_id_ingredient = rq.get_amount_with_name(request.form.get("ingredient"))
        get_id_amount = session.query(Amount).filter(Amount.amount == request.form.get("amount")).first()
        get_new_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
            desc(Recipe.version)).first()
        if get_id_ingredient is None:
            add_ingredient = Ingredient(name=request.form.get("ingredient"))
            session.add(add_ingredient)
            session.commit()
        if get_id_amount is None:
            add_amount = Amount(amount=request.form.get("amount"))
            session.add(add_amount)
            session.commit()
        measurement_id = session.query(Measurement.id).filter(Measurement.name == request.form.get("unit")).first()
        ingredient_id = session.query(Ingredient.id).filter(Ingredient.name == request.form.get("ingredient")).first()
        measurement_and_ingredient_check = session.query(Recipe_ingredient_helper).filter(
            Recipe_ingredient_helper.measurement_id == measurement_id.id,
            Recipe_ingredient_helper.ingredient_id == ingredient_id.id,
            Recipe_ingredient_helper.recipe_id == get_new_recipe_version.id).first()
        if measurement_and_ingredient_check:
            get_old_amount = session.query(Amount).filter(
                Amount.id == measurement_and_ingredient_check.amount_id).first()

            get_new_amount = int(request.form.get("amount"))

            sum_amount = get_old_amount.amount + get_new_amount
            check_new_amount = session.query(Amount).filter(
                Amount.amount == sum_amount).first()
            if not check_new_amount:
                add_amount = Amount(amount=sum_amount)
                session.add(add_amount)
                session.commit()
            new_amount_id = session.query(Recipe_ingredient_helper).filter(
                Recipe_ingredient_helper.recipe_id == get_new_recipe_version.id,
                Recipe_ingredient_helper.ingredient_id == ingredient_id.id).first()
            tullekoppen = session.query(Amount).filter(Amount.amount == sum_amount).first()
            new_amount_id.amount_id = tullekoppen.id
            session.add(new_amount_id)
            session.commit()
        else:
            ingredient = session.query(Ingredient).filter(Ingredient.name == request.form.get("ingredient")).first()

            amount = session.query(Amount).filter(Amount.amount == request.form.get("amount")).first()

            measurement = session.query(Measurement).filter(Measurement.name == request.form.get("unit")).first()

            recipe = session.query(Recipe).filter(
                Recipe.approach == get_new_recipe_version.approach).first()

            add_ids_to_helper_table = Recipe_ingredient_helper(recipe=recipe, measurement=measurement,
                                                               amount=amount,
                                                               ingredient=ingredient)
            session.add(add_ids_to_helper_table)
            session.commit()
    if "ingredient_name" in request.form:
        recipe_id = session.query(Recipe.id).filter(Recipe.dinner_id == dinner_id).order_by(
            desc(Recipe.version)).first()
        delete_ingredient = session.query(Ingredient).filter(
            Ingredient.name == request.form.get("ingredient_name")).first()
        session.close()
        delete_measurement = session.query(Measurement).filter(
            Measurement.name == request.form.get("measurement_name")).first()
        session.close()
        delete_data = session.query(Recipe_ingredient_helper).filter(
            Recipe_ingredient_helper.ingredient_id == delete_ingredient.id,
            Recipe_ingredient_helper.recipe_id == recipe_id.id,
            Recipe_ingredient_helper.measurement_id == delete_measurement.id).first()
        session.delete(delete_data)
        session.commit()

    if "btnVidere" in request.form:
        session.commit()
        session.close()
        return redirect(url_for('grouproute.show_group', group_id=group_id))
    return redirect(url_for('recipe_route.change_recipe', dinner_id=dinner_id, group_id=group_id))
