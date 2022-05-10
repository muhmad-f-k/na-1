from sqlalchemy import desc

from db.modul import *


def get_highest_recipe_version_with_dinner_id(dinner_id):
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version


def add_new_version_to_recipe(approach, dinner_id):
    highest_recipe_version = get_highest_recipe_version_with_dinner_id(dinner_id)
    Recipe(approach=approach,
           version=highest_recipe_version.version + 1,
           dinner_id=dinner_id,
           portions=highest_recipe_version.portions)
    session.add(add_new_version_to_recipe)
    session.commit()
    return


def get_ingredients_with_highest_recipe_version(highest_recipe_version):
    return session.query(Ingredient.id).join(
        Recipe_ingredient_helper).filter(
        Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_amounts_with_highest_recipe_version(highest_recipe_version):
    return session.query(Amount.id).join(Recipe_ingredient_helper).filter(
        Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_measurement_with_highest_recipe_version(highest_recipe_version):
    return session.query(Measurement.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_ingredient_with_name(ingredient):
    session.query(Ingredient).filter(Ingredient.name == ingredient).first()
