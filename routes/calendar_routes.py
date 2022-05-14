import base64
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, login_required, current_user, logout_user
from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import desc, func, cast, Float, DECIMAL
from base64 import b64encode
from db.modul import *
from flask_login import current_user
from datetime import date, timedelta, datetime
import queries
import routes.calendar_methods as calendar_methods

calendarroute = Blueprint('calendarroute', __name__)


@calendarroute.route('/calendar')
def show_calendar():
    import datetime
    import isoweek

    def add_portions(portion):
        portion += 1
        return portion

    def subtract_portions(portion):
        portion -= 1
        return portion

    if request.args.get('group_name'):
        # group_id = int(request.args.get('group_id'))
        group_name = request.args.get('group_name')
        print(group_name)
        group_id = calendar_methods.get_group(group_name).id
        # group_name = calendar_methods.get_group_name(group_id)
    else:
        group_name = 'Resturant Matmons'
        group_id = calendar_methods.get_group(group_name).id

    days_of_week = calendar_methods.day_strings()
    incoming_year, incoming_week_number = calendar_methods.interact_with_calendar(request)
    days_to_cal, year_to_cal, week_number_to_cal = calendar_methods.get_days_and_week_and_year(incoming_week_number,
                                                                                               incoming_year)
    meals = calendar_methods.get_meals(days_to_cal, group_id)
    dinners = calendar_methods.get_dinners(meals)
    user_group_role = calendar_methods.get_user_role(group_id)

    return render_template('groups/calendar.html', days_of_week=days_of_week, days_to_cal=days_to_cal,
                           year_to_cal=int(year_to_cal), week_number_to_cal=int(week_number_to_cal),
                           group_name=group_name, user_group_role=user_group_role,
                           group_id=group_id, dinners=dinners, meals=meals, add_portions=add_portions,
                           subtract_portions=subtract_portions)

@calendarroute.route('/calendar', methods=['POST'])
def show_calendar_post():
    import datetime
    import isoweek

    def add_portions(portion):
        portion += 1
        return portion

    def subtract_portions(portion):
        portion -= 1
        return portion

    if request.args.get('group_name'):
        # group_id = int(request.args.get('group_id'))
        group_name = request.args.get('group_name')
        print(group_name)
        group_id = calendar_methods.get_group(group_name).id
        # group_name = calendar_methods.get_group_name(group_id)
    else:
        group_name = 'Resturant Matmons'
        group_id = calendar_methods.get_group(group_name).id

    days_of_week = calendar_methods.day_strings()
    incoming_year, incoming_week_number = calendar_methods.interact_with_calendar(request)
    days_to_cal, year_to_cal, week_number_to_cal = calendar_methods.get_days_and_week_and_year(incoming_week_number,
                                                                                               incoming_year)
    meals = calendar_methods.get_meals(days_to_cal, group_id)
    dinners = calendar_methods.get_dinners(meals)
    user_group_role = calendar_methods.get_user_role(group_id)

    return render_template('groups/calendar.html', days_of_week=days_of_week, days_to_cal=days_to_cal,
                           year_to_cal=int(year_to_cal), week_number_to_cal=int(week_number_to_cal),
                           group_name=group_name, user_group_role=user_group_role,
                           group_id=group_id, dinners=dinners, meals=meals, add_portions=add_portions,
                           subtract_portions=subtract_portions)


@calendarroute.route('/createMeal')
def create_meal():
    return render_template('groups/add_dinner_to_calendar.html')


@calendarroute.route('/createMeal', methods=['POST'])
def create_meal_post():
    if "choose_dinner" in request.form:
        inc_year, week_number, group_id = calendar_methods.choose_dinner(request)
        group_name = calendar_methods.get_group_name(group_id)
        return redirect(url_for('calendarroute.show_calendar',
                                create_meal_year=inc_year, create_meal_week_number=week_number, group_id=group_id,
                                group_name=group_name))
    else:
        inc_year, inc_month, inc_day, conv_dinners, group_id = calendar_methods.add_dinner(request)
        group_name = calendar_methods.get_group_name(group_id)
        return render_template('groups/add_dinner_to_calendar.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day,
                               dinners=conv_dinners, group_id=group_id, group_name=group_name)


@calendarroute.route('/createDinner/<group_id>')
def create_dinner(group_id):
    current_user_role = calendar_methods.get_current_user_role(group_id)
    return render_template('dinners/create_dinner.html', current_user_role=current_user_role)


@calendarroute.route('/createDinner/<group_id>', methods=['POST'])
def create_dinner_post(group_id):
    dinner = calendar_methods.create_dinner(current_user, group_id)
    return redirect(url_for(
        "recipe_route.createRecipe", dinner_id=dinner.id))


@calendarroute.route('/show_group_dinners/<group_id>')
def show_group_dinners(group_id):
    dinners = session.query(Dinner).filter(Dinner.group_id == group_id).all()

    def decode_image(image):
        picture = b64encode(image).decode("utf-8")
        return picture

    # image = b64encode(dinners.image).decode("utf-8")

    session.close()
    return render_template("dinners.html", dinners=dinners, group_id=group_id, decode_image=decode_image)


@calendarroute.route('/show_dinner/<dinner_id>/<group_id>')
def show_dinner(dinner_id, group_id):
    dinner, current_user_role, recipe, image, ingredients_recipe, amounts_recipe, measurements_recipe, comments, comments_users, image2, decode_image = calendar_methods.get_detailed_dinner(current_user, dinner_id, group_id)
    dinner, current_user_role, recipe, image, ingredients_recipe, amounts_recipe, measurements_recipe, comments, comments_users, image2, decode_image
    return render_template("dinners/dinner.html", dinner=dinner,
                           group_id=group_id,
                           dinner_id=dinner_id,
                           current_user_role=current_user_role,
                           len=len(ingredients_recipe),
                           recipe=recipe, image=image,
                           ingredients=ingredients_recipe,
                           amounts=amounts_recipe,
                           measurements=measurements_recipe,
                           comments=comments,
                           c_len=len(comments),
                           comments_users=comments_users,
                           image2=image2,
                           decode_image=decode_image)


@calendarroute.route('/shopping_list/<group_id>')
def show_shopping_list(group_id):
    headings, data, week_number, add_days, subtract_days, new_date, year, shopping_list, current_user_role = calendar_methods.get_shopping_list(group_id)
    return render_template('groups/shopping_list.html', headings=headings, data=data, group_id=group_id,
                           week_number=week_number, add_days=add_days, subtract_days=subtract_days,
                           new_date=new_date, year=new_date.year, shopping_list=shopping_list,
                           current_user_role=current_user_role)


@calendarroute.route('/shopping_list/<group_id>', methods=['POST'])
def show_shopping_list_post(group_id):
    headings, data, week_number, add_days, subtract_days, new_date, year, shopping_list, current_user_role = calendar_methods.get_shopping_list(group_id)
    return render_template('groups/shopping_list.html', headings=headings, data=data, group_id=group_id,
                           week_number=week_number, add_days=add_days, subtract_days=subtract_days,
                           new_date=new_date, year=new_date.year, shopping_list=shopping_list,
                           current_user_role=current_user_role)


@calendarroute.route('/show_dinner/<dinner_id>/<group_id>', methods=['POST'])
@login_required
def comment_post(dinner_id, group_id):
    calendar_methods.comment_post(request, dinner_id, group_id)
    return redirect(url_for("calendarroute.show_dinner", dinner_id=dinner_id, group_id=group_id))
