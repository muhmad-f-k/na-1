from flask import Blueprint, render_template, request, url_for, flash
from db.modul import *
from sqlalchemy import Float
from sqlalchemy.sql import func, cast
from collections import Counter

rapportroute = Blueprint('rapportroute', __name__)


@rapportroute.route("/report/<group_id>")
def report(group_id):
    """render report page"""

    return render_template("groups/report.html", group_id=group_id)


@rapportroute.route("/report/<group_id>", methods=['POST'])
def report_post(group_id):
    """Gets data from database based on start and end date. """
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    headings = ("Ingredient", "measurement", "amount")
    data = session.query(Ingredient.name, func.sum(
        cast(Amount.amount, Float) / Recipe.portions * Meal.portions), Measurement.name).select_from(
        Meal).join(Dinner).join(Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement). \
        join(Amount).filter(Dinner.id == Meal.dinner_id, Meal.group_id == group_id,
                            Meal.date.between(start_date, end_date)).group_by(Ingredient.name, Measurement.name).all()
    """This generate headings for the html table"""
    headings1 = ("Total Pris",)
    total_price = session.query(func.sum(Shopping_list.price).label('Total Pris')).filter(
        Shopping_list.date.between(start_date, end_date), Shopping_list.group_id == group_id).all()
    session.close()
    list = []
    """This generate top 3 dinners based on total most common dinners in the database"""
    headings2 = ("Top 3 Middag",)
    top_3_dinner = session.query(Dinner.title).select_from(
        Group).join(Dinner).join(Meal).filter(Meal.date.between(start_date, end_date), Meal.group_id == group_id).all()
    """This is the counter for the top 3 dinners"""
    count = Counter(top_3_dinner)
    top_3_dinner_result = count.most_common(3)
    list.append(top_3_dinner_result)
    return render_template("groups/report.html", headings=headings, data=data, headings1=headings1, data1=total_price, headings2=headings2, data2=list, group_id=group_id)
