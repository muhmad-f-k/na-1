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
    headings = ("Ingredient", "measurement", "amount")
    data = session.query(Ingredient.name, Measurement.name, Amount.amount).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement).join(Amount).filter(Dinner.id == Recipe.dinner_id, Dinner.group_id == 1).all()
    return render_template("report_result.html", headings=headings, data=data)
