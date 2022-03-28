from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import *
from flask_login import current_user

ingredientroute = Blueprint('ingredient', __name__)


@ingredientroute.route("/ingredient")
def ingredient():
    ingredients = session.query(Ingredient)
    name = current_user.first_name

    return render_template('ingredient.html', name=name, ingredients=ingredients)


@ingredientroute.route("/ingredient", methods=['POST'])
def ingredient_post():

    name = request.form.get("ingredient__name")
    print(name)

    user = session.query(Ingredient).filter(Ingredient.name == name).first()
    print(user)
    if user:
        flash("ingrediens finnes allerede.")
        return redirect(url_for("ingredient.ingredient"))

    new_user = Ingredient(name=name)
    session.add(new_user)
    session.commit()

    return redirect(url_for("ingredient.ingredient"))
