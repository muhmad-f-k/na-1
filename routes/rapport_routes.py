from urllib import robotparser
from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import *
from sqlalchemy.sql import func
from flask_login import current_user
from collections import Counter

rapportroute = Blueprint('rapportroute', __name__)


@rapportroute.route("/report")
def report():
    return render_template("report.html")


@rapportroute.route("/report", methods=['POST'])
def report_post():
    user = current_user
    groups = session.query(Group.id).join(
        User_group_role).join(User).filter(User.id == user.id).first()
# husk å endre til å ta gruppe id
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    total_price = session.query(func.sum(Shopping_list.price).label('Total Pris')).filter(
        Shopping_list.date.between(start_date, end_date), Shopping_list.group_id == groups.id).all()
    session.close()
# husk å endre til å ta gruppe id
    top_3_dinner = session.query(Dinner.title).select_from(
        Group).join(Dinner).join(Meal).filter(Meal.date.between(start_date, end_date), Meal.group_id == 1).all()

    count = Counter(top_3_dinner)
    top_3_dinner_result = count.most_common(3)
# husk å endre til å ta gruppe id
    ingredient = session.query(Ingredient.name).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Measurement).join(Ingredient).join(Amount).filter(Meal.date.between(start_date, end_date), Meal.dinner_id == 1).all()

    measurement = session.query(Measurement.name).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Measurement).join(Ingredient).join(Amount).filter(Meal.date.between(start_date, end_date), Meal.dinner_id == 1).all()

    amount = session.query(Amount.amount).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Measurement).join(Ingredient).join(Amount).filter(Meal.date.between(start_date, end_date), Meal.dinner_id == 1).all()

    print(ingredient)
    print(measurement)
    print(amount)
    return render_template("report_result.html", cost=total_price, top_3_dinner=top_3_dinner_result, data=ingredient, data1=measurement, data2=amount)


@ rapportroute.route("/rapport_ingredient", methods=['POST'])
def rapport_ingredient_post():
    user = current_user
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    # Sjekk med dato ved å bruk meal table
    ingredient = session.query(Ingredient.name).filter(Meal.date.between(start_date, end_date), Dinner.id == Meal.dinner_id,
                                                       user.id == User_group_role.user_id, User_group_role.group_id == Group.id, Group.id == Dinner.group_id, Dinner.id == Recipe.dinner_id, Recipe.id == Recipe_ingredient_helper.recipe_id, Recipe_ingredient_helper.ingredient_id == Ingredient.id).all()

    measurement = session.query(Measurement.name).filter(
        user.id == User_group_role.user_id, User_group_role.group_id == Group.id, Group.id == Dinner.group_id, Dinner.id == Recipe.dinner_id, Recipe.id == Recipe_ingredient_helper.recipe_id, Recipe_ingredient_helper.measurement_id == Measurement.id).all()

    amount = session.query(Amount.amount).filter(
        user.id == User_group_role.user_id, User_group_role.group_id == Group.id, Group.id == Dinner.group_id, Dinner.id == Recipe.dinner_id, Recipe.id == Recipe_ingredient_helper.recipe_id, Recipe_ingredient_helper.amount_id == Amount.id).all()
    return render_template("result_ingredient.html", data=ingredient, data1=measurement, data2=amount)
