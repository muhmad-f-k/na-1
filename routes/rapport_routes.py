import re
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
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    headings = ("Ingredient", "measurement", "amount")
    data = session.query(Ingredient.name, Measurement.name, Amount.amount).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement).join(Amount).filter(Dinner.id == Recipe.dinner_id, Dinner.group_id == Meal.group_id, Meal.date.between(start_date, end_date)).all()
    session.close()

    headings1 = ("Total Pris", "")
    total_price = session.query(func.sum(Shopping_list.price).label('Total Pris')).filter(
        Shopping_list.date.between(start_date, end_date), Shopping_list.group_id == 1).all()
    session.close()
    list = []

    headings2 = ("Top 3 Middag", "")
    top_3_dinner = session.query(Dinner.title).select_from(
        Group).join(Dinner).join(Meal).filter(Meal.date.between(start_date, end_date)).all()

    count = Counter(top_3_dinner)
    top_3_dinner_result = count.most_common(3)
    list.append(top_3_dinner_result)
    return render_template("report_result.html", headings=headings, data=data, headings1=headings1, data1=total_price, headings2=headings2, data2=list)
