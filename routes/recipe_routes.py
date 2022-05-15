from base64 import b64encode

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user

import queries as rq
from db.modul import *
from sqlalchemy import desc

recipe_route = Blueprint('recipe_route', __name__)


@recipe_route.route('/create_recipe/<dinner_id>')
def create_recipe(dinner_id):
    return render_template('dinners/create_recipe.html', dinner_id=dinner_id)


@recipe_route.route('/create_recipe/<dinner_id>', methods=['POST'])
def create_recipe_post(dinner_id):
    approach = str(request.form.get("dinner-approach"))
    portions = int(request.form.get("portions"))

    recipe_object = rq.add_new_recipe(approach, dinner_id, portions)
    print('Recipe id ' + str(recipe_object.id))
    return redirect(url_for("recipe_route.add_ingredients", recipe_id=recipe_object.id, dinner_id=dinner_id))


@recipe_route.route("/add_ingredients/<recipe_id>")
def add_ingredients(recipe_id):
    measurements = rq.get_all_measurements()

    ingredients_recipe = rq.get_ingredient_names_with_recipe_id(recipe_id)
    amounts_recipe = rq.get_amount_amounts_with_recipe_id(recipe_id)
    measurements_recipe = rq.get_measurement_measurements_with_recipe_id(recipe_id)
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
    dinner = rq.get_dinner_object_with_dinner_id(dinner_id)
    #                     --nåværende versjon--

    recipe_versions = rq.get_highest_recipe_versions_with_dinner_id(dinner_id)
    current_version_id = recipe_versions[0].id

    # henter oppskrift, ingredienser, mengder og måleenheter
    recipe = session.query(Recipe).filter(Recipe.id == current_version_id).first()
    ingredients_recipe = rq.get_ingredient_names_with_recipe_id(current_version_id)
    amounts_recipe = rq.get_amount_amounts_with_recipe_id(current_version_id)
    measurements_recipe = rq.get_measurement_measurements_with_recipe_id(current_version_id)

    #                  --tidligere versjon--
    ingredients_recipe_prev = ""
    amounts_recipe_prev = ""
    measurements_recipe_prev = ""
    recipe_prev = ""
    len_prev = 0
    ingredient_status = ""
    approach_status = ""
    if len(recipe_versions) < 2:
        print('Det finnes kun en versjon av denne')
        approach_status = "Det finnes ingen tidligere versjoner av denne oppskriften"
        ingredient_status = "Det finnes ingen tidligere versjoner av denne oppskriften"
    elif len(recipe_versions) == 2 or len(recipe_versions) > 2:
        previous_version_id = recipe_versions[1].id
        print('det finnes flere versjoner')
        recipe_prev = session.query(Recipe).filter(
            Recipe.id == previous_version_id).first()

        # henter oppskrift, ingredienser, mengder og måleenheter
        ingredients_recipe_prev = rq.get_ingredient_names_with_recipe_id(previous_version_id)

        amounts_recipe_prev = rq.get_amount_amounts_with_recipe_id(previous_version_id)

        measurements_recipe_prev = rq.get_measurement_measurements_with_recipe_id(previous_version_id)

        # fastsetter størrelsen av ingrediens-listen
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
    current_user_role = rq.get_user_group_role(current_user.id, group_id)

    dinner = rq.session.query(Dinner).filter(Dinner.id == dinner_id).first()
    # nåværende
    recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).all()
    current_version_id = recipe_version[0].id

    # henter oppskrift, ingredienser, mengder og måleenheter
    recipe = session.query(Recipe).filter(Recipe.id == current_version_id).first()
    ingredients_recipe = rq.get_ingredient_names_with_recipe_id(current_version_id)
    amounts_recipe = rq.get_amount_amounts_with_recipe_id(current_version_id)
    measurements_recipe = rq.get_measurement_measurements_with_recipe_id(current_version_id)
    measurement_recipe_helper = measurements_recipe

    measurements = rq.get_all_measurements()

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
        original_ingredients = rq.get_ingredient_ids_with_highest_recipe_version(highest_recipe_version.id)
        original_amounts = rq.get_amount_ids_with_highest_recipe_version(highest_recipe_version.id)
        original_measurements = rq.get_measurement_ids_with_highest_recipe_version(highest_recipe_version.id)

        rq.copy_recipe_ingredient_helper(new_highest_version, original_ingredients, original_amounts, original_measurements)

    if "ingredient" in request.form:
        amount = request.form.get("amount")
        ingredient = request.form.get("ingredient")
        measurement = request.form.get("unit")

        # sjekk om ingrediens ligger i tabell, hvis ikke legg til
        rq.check_ingredient_in_table_and_get_object(ingredient)
        # sjekk om amount ligger i tabell, hvis ikke legg til
        rq.check_amount_in_table_and_get_object(amount)
        # få tak i nyeste versjon
        get_new_recipe_version = rq.get_highest_recipe_version_with_dinner_id(dinner_id)
        measurement_id = session.query(Measurement.id).filter(Measurement.name == request.form.get("unit")).first()
        ingredient_id = rq.check_ingredient_in_table_and_get_object(ingredient).id

        measurement_and_ingredient_check = session.query(Recipe_ingredient_helper).filter(
            Recipe_ingredient_helper.measurement_id == measurement_id.id,
            Recipe_ingredient_helper.ingredient_id == ingredient_id,
            Recipe_ingredient_helper.recipe_id == get_new_recipe_version.id).first()
        if measurement_and_ingredient_check:
            get_old_amount = session.query(Amount).filter(
                Amount.id == measurement_and_ingredient_check.amount_id).first()

            check_new_amount = rq.sum_up_amounts_and_get_object(get_old_amount.amount, int(amount))

            new_amount_id = session.query(Recipe_ingredient_helper).filter(
                Recipe_ingredient_helper.recipe_id == get_new_recipe_version.id,
                Recipe_ingredient_helper.measurement_id == measurement_id.id,
                Recipe_ingredient_helper.ingredient_id == ingredient_id).first()
            tullekoppen = session.query(Amount).filter(Amount.amount == check_new_amount.amount).first()
            new_amount_id.amount_id = tullekoppen.id
            session.add(new_amount_id)
            session.commit()

        else:
            ingredient = session.query(Ingredient).filter(Ingredient.name == request.form.get("ingredient")).first()

            amount = session.query(Amount).filter(Amount.amount == request.form.get("amount")).first()

            measurement = session.query(Measurement).filter(Measurement.name == request.form.get("unit")).first()

            add_ids_to_helper_table = Recipe_ingredient_helper(recipe=get_new_recipe_version, measurement=measurement,
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