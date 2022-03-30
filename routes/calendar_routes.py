from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import desc
from base64 import b64encode
from db.modul import *
from flask_login import current_user

calendarroute = Blueprint('calendarroute', __name__)

""" @calendarroute.route('/calendar')
def calendar():
    return render_template("calendar.html") """


@calendarroute.route('/calendar', methods=['GET', 'POST'])
def show_calendar():
    import calendar as cd
    import datetime

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

    current_date_time = None
    if new_year is not None and new_month is not None:
        current_date_time = datetime.datetime(new_year, new_month, 1)
    else:
        current_date_time = datetime.datetime.now()

    year = current_date_time.year
    month = current_date_time.month
    month_name = months_of_year.get(current_date_time.strftime("%B"))

    c = cd.Calendar(firstweekday=0)
    full_month = []
    for i in c.itermonthdates(year, month):
        if i.month != month:
            pass
        else:
            full_month.append(i)
    return render_template('calendar.html',
                           days_of_week=days_of_week, full_month=full_month, year=year, month=month,
                           month_name=month_name)


@calendarroute.route('/createMeal', methods=['GET', 'POST'])
def create_meal():
    import calendar as cd
    import datetime

    if "dinner_id" in request.form:
        dinner_id = request.form.get('dinner_id')
        incoming_date = request.form.get('date')

        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        meal_date = datetime.datetime(inc_year, inc_month, inc_day)

        meal = Meal(date=meal_date, dinner_id=dinner_id)
        session.add(meal)
        session.commit()
        session.close()
        return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day)
    else:
        incoming_date = request.form.get("add_dinner")
        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        # current_date_time = datetime.datetime(inc_year, inc_month, inc_day)
        # print(str(inc_year) + ' ' + str(inc_month) + ' ' + str(inc_day))
        # print(current_date_time)
        return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day)


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


@calendarroute.route('/deleteDinner', methods=['GET', 'POST'])
def delete_dinner():
    if 'dinner_id' in request.form:
        session.query(Dinner).filter_by(id=request.form.get('dinner_id')).delete()
        session.commit()
    return render_template("deleteDinner.html")

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


@calendarroute.route('/shopping_list/<group_id>')
def show_shopping_list(group_id):
    ingredients_week = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).join(Dinner).join(Meal).filter(Meal.group_id == group_id, Meal.date)

    return render_template("shopping_list.html", group_id=group_id)



