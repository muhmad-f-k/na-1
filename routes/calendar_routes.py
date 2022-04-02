import base64
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, login_required, current_user, logout_user
from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import desc
from base64 import b64encode
from db.modul import *
from flask_login import current_user
from datetime import date, timedelta, datetime
from collections import defaultdict


calendarroute = Blueprint('calendarroute', __name__)

""" @calendarroute.route('/calendar')
def calendar():
    return render_template("calendar.html") """


@calendarroute.route('/calendar', methods=['GET', 'POST'])
def show_calendar():
    import calendar as cd
    import datetime
    import base64

    group_id = 1
    group_name = None
    if request.args.get('group_id'):
        group_id = int(request.args.get('group_id'))
        group_name = session.query(Group).filter_by(id=group_id).first().name
    else:
        group_name = group_name = session.query(Group).filter_by(id=group_id).first().name

    days_of_week = {"Monday": "Mandag",
                    "Tuesday": "Tirsdag",
                    "Wednesday": "Onsdag",
                    "Thursday": "Torsdag",
                    "Friday": "Fredag",
                    "Saturday": "Lørdag",
                    "Sunday": "Søndag"}

    months_of_year = {"January": "Januar",
                      "February": "Februar",
                      "March": "Mars",
                      "April": "April",
                      "May": "Mai",
                      "June": "Juni",
                      "July": "Juli",
                      "August": "August",
                      "September": "September",
                      "October": "Oktober",
                      "November": "November",
                      "December": "Desember"}

    new_year = None
    new_month = None
    if "next_month" in request.form:
        incoming_date = request.form.get("next_month")
        converted_date = incoming_date.strip('][').split(', ')
        new_year = int(converted_date[0])
        new_month = int(converted_date[1])
        if new_month > 12:
            new_year += 1
            new_month = 1
    elif "prev_month" in request.form:
        incoming_date = request.form.get("prev_month")
        converted_date = incoming_date.strip('][').split(', ')
        new_year = int(converted_date[0])
        new_month = int(converted_date[1])
        if new_month < 1:
            new_year -= 1
            new_month = 12

    elif 'delete_meal' in request.form:
        incoming_date = request.form.get("delete_meal")
        converted_date = incoming_date.strip('][').split(', ')
        meal_id = int(converted_date[0])
        new_year = int(converted_date[1])
        new_month = int(converted_date[2])

        session.query(Meal).filter_by(id=meal_id).delete()
        session.commit()
        session.close()

    elif request.args.get('create_meal_year') and request.args.get('create_meal_month'):
        incoming_date = [request.args.get('create_meal_year'), request.args.get('create_meal_month')]
        # print(incoming_date)
        new_year = int(incoming_date[0])
        new_month = int(incoming_date[1])

    current_date_time = None
    if new_year is not None and new_month is not None:
        current_date_time = datetime.datetime(new_year, new_month, 1)
    else:
        current_date_time = datetime.datetime.now()

    year = current_date_time.year
    month = current_date_time.month
    month_name = months_of_year.get(current_date_time.strftime("%B"))

    meals = []
    c = cd.Calendar(firstweekday=0)
    full_month = []
    for i in c.itermonthdates(year, month):
        if i.month != month:
            pass
        else:
            full_month.append(i)
            if group_id:
                meals.append(
                    session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(Meal.group_id == group_id).filter(Meal.date == i).first())
                session.close()
            else:
                meals.append(
                    session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(Meal.date == i).first())
                session.close()

    dinners = []
    for n in meals:
        if n:
            ddinner = n[1]
            title = ddinner.title
            dimage = base64.b64encode(ddinner.image).decode("utf-8")
            dinners.append([title, dimage])
        else:
            dinners.append(n)

    return render_template('calendar.html',
                           days_of_week=days_of_week, full_month=full_month, year=year, month=month,
                           month_name=month_name, dinners=dinners, meals=meals, group_id=group_id, group_name=group_name)


@calendarroute.route('/createMeal', methods=['GET', 'POST'])
def create_meal():
    import datetime

    if "choose_dinner" in request.form:
        dinner_id = request.form.get('choose_dinner')

        converted_date = dinner_id.strip('][').split(', ')
        inc_dinner_id = int(converted_date[0])
        inc_year = int(converted_date[1])
        inc_month = int(converted_date[2])
        inc_day = int(converted_date[3])
        group_id = int(converted_date[4])
        meal_date = datetime.datetime(inc_year, inc_month, inc_day)

        meal = Meal(date=meal_date, dinner_id=inc_dinner_id, group_id=group_id)
        session.add(meal)
        session.commit()
        session.close()
        return redirect(url_for('calendarroute.show_calendar',
                                create_meal_year=inc_year, create_meal_month=inc_month, group_id=group_id))
    else:
        incoming_date = request.form.get("add_dinner")
        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        group_id = int(converted_date[3])
        dinners = session.query(Dinner).filter_by(group_id=group_id).all()
        session.close()

        conv_dinners = []
        for dinner in dinners:
            # print(dinner)
            did = dinner.id
            title = dinner.title
            dimage = base64.b64encode(dinner.image).decode("utf-8")
            conv_dinners.append([did, title, dimage])

        return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day,
                               dinners=conv_dinners, group_id=group_id)



@calendarroute.route('/deleteDinner', methods=['GET', 'POST'])
def delete_dinner():
    if 'dinner_id' in request.form:
        session.query(Dinner).filter_by(id=request.form.get('dinner_id')).delete()
        session.commit()
        session.close()
    return render_template("deleteDinner.html")


@calendarroute.route('/deleteMeal', methods=['GET', 'POST'])
def delete_meal():
    if 'meal_id' in request.form:
        session.query(Meal).filter_by(id=request.form.get('meal_id')).delete()
        session.commit()
        session.close()
    return render_template("deleteMeal.html")


@calendarroute.route('/createDinner/<group_id>')
def create_dinner(group_id):
    current_user_role = session.query(User_group_role).filter(
        User_group_role.user_id == current_user.id,
        User_group_role.group_id == group_id).first()

    return render_template('createDinner.html', current_user_role=current_user_role)


@calendarroute.route('/createDinner/<group_id>', methods=['POST'])
def create_dinner_post(group_id):
    dinner_title = request.form.get('dinner_title')
    user_id = current_user.id
    dinner_image = request.files['dinner_image'].read()
    print(dinner_image)

    dinner = Dinner(title=dinner_title, image=dinner_image, user_id=user_id, group_id=group_id)
    session.add(dinner)
    session.commit()
    return redirect(url_for(
        "recipe_route.createRecipe", dinner_id=dinner.id))


@calendarroute.route('/show_group_dinners/<group_id>')
def show_group_dinners(group_id):
    dinners = session.query(Dinner).filter(Dinner.group_id == group_id).all()

    def decode_image(image):
        picture = b64encode(image).decode("utf-8")
        return picture

    #image = b64encode(dinners.image).decode("utf-8")

    session.close()
    return render_template("dinners.html", dinners=dinners, group_id=group_id, decode_image=decode_image)


@calendarroute.route('/show_dinner/<dinner_id>/<group_id>')
def show_dinner(dinner_id, group_id):
    current_user_role = session.query(User_group_role).filter(
        User_group_role.user_id == current_user.id,
        User_group_role.group_id == group_id).first()
    dinner = session.query(Dinner).filter(Dinner.id == dinner_id).first()
    recipe = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(desc(Recipe.version)).first()

    image = b64encode(dinner.image).decode("utf-8")

    ingredients_recipe = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()
    session.close()
    amounts_recipe = session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()
    session.close()
    measurements_recipe = session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()
    session.close()

    return render_template("dinner.html", dinner=dinner,
                           current_user_role=current_user_role,
                           len=len(ingredients_recipe),
                           recipe=recipe, image=image,
                           ingredients=ingredients_recipe,
                           amounts=amounts_recipe,
                           measurements=measurements_recipe)


@calendarroute.route('/shopping_list/<group_id>', methods=['GET', 'POST'])
def show_shopping_list(group_id):
    today = date.today()

    def add_days(date):
        date += timedelta(days=7)
        return date

    def subtract_days(date):
        date -= timedelta(days=7)
        return date

    if "next_week" in request.form:
        incoming_date = request.form.get("next_week")
        new_date = date.fromisoformat(incoming_date)

    elif "prev_week" in request.form:
        incoming_date = request.form.get("prev_week")
        new_date = date.fromisoformat(incoming_date)

    else:
        new_date = today

    weekday = new_date.weekday()
    monday = new_date - timedelta(days=weekday)
    sunday = new_date + timedelta(6 - weekday)

    week_number = datetime(new_date.year, new_date.month, new_date.day).isocalendar()[1]
    list = []
    headings = ("Ingrediens", "mengde", "Enhet")
    data = session.query(Ingredient.name, Measurement.name, Amount.amount).select_from(
        Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement).join(Amount).filter(Dinner.id == Recipe.dinner_id, Dinner.group_id == Meal.group_id, Meal.date.between(monday, sunday)).all()
    for lists in data:
        list.append(lists)
    # my_list = defaultdict(list)
    # print(my_list)
    print(list)

    session.close()

    return render_template("shopping_list.html", headings=headings, data=data, group_id=group_id,
                           week_number=week_number, add_days=add_days, subtract_days=subtract_days,
                           new_date=new_date)
    # ingredients_week = session.query(Ingredient.name).join(
    #     Recipe_ingredient_helper).join(Recipe).join(Dinner).join(Meal).filter(
    #     Meal.date.between(monday, sunday), Meal.group_id == group_id).all()
    #
    # amounts_week = session.query(Amount.amount).join(
    #     Recipe_ingredient_helper).join(Recipe).join(Dinner).join(Meal).filter(
    #     Meal.date.between(monday, sunday), Meal.group_id == group_id).all()
    #
    # measurements_week = session.query(Measurement.name).join(
    #     Recipe_ingredient_helper).join(Recipe).join(Dinner).join(Meal).filter(
    #     Meal.date.between(monday, sunday), Meal.group_id == group_id).all()

    # return render_template("shopping_list.html", group_id=group_id, ingredients=ingredients_week,
    #                        measurements=measurements_week, amounts=amounts_week, week_number=week_number,
    #                        len=len(ingredients_week), add_days=add_days, subtract_days=subtract_days,
    #                        new_date=new_date)

    # if "next_month" in request.form:
    #     incoming_date = request.form.get("next_month")
    #     converted_date = incoming_date.strip('][').split(', ')
    #     new_year = int(converted_date[0])
    #     new_month = int(converted_date[1])
    #     if new_month > 12:
    #         new_year += 1
    #         new_month = 1
    # elif "prev_month" in request.form:
    #     incoming_date = request.form.get("prev_month")
    #     converted_date = incoming_date.strip('][').split(', ')
    #     new_year = int(converted_date[0])
    #     new_month = int(converted_date[1])
    #     if new_month < 1:
    #         new_year -= 1
    #         new_month = 12
    #
    # current_date_time = None
    # if new_year is not None and new_month is not None:
    #     current_date_time = datetime.datetime(new_year, new_month, 1)
    # else:
    #     current_date_time = datetime.datetime.now()
    #
    # year = current_date_time.year
    # month = current_date_time.month
    # month_name = months_of_year.get(current_date_time.strftime("%B"))



