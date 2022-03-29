import base64
import io

from flask import Blueprint, render_template, request, url_for
from db.modul import *

calendarroute = Blueprint('calendarroute', __name__)

""" @calendarroute.route('/calendar')
def calendar():
    return render_template("calendar.html") """


@calendarroute.route('/calendar', methods=['GET', 'POST'])
def show_calendar():
    import calendar as cd
    import datetime
    import base64
    import matplotlib.pyplot as plt
    from PIL import Image
    import io

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

    meals = []
    c = cd.Calendar(firstweekday=0)
    full_month = []
    for i in c.itermonthdates(year, month):
        if i.month != month:
            pass
        else:
            # print('' + str(i) + ' ' + str(type(i)))
            full_month.append(i)
            # print(i)

            # get dinners for this month
            # meals.append(session.query(Meal).filter(Meal.date == str(i)).first())
            meals.append(session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(Meal.date == i).first())
            session.close()
    dinner = meals[2][1]
    image = base64.b64encode(dinner.image).decode("utf-8")

    return render_template('calendar.html',
                           days_of_week=days_of_week, full_month=full_month, year=year, month=month,
                           month_name=month_name, meals=meals, image=image)


@calendarroute.route('/createMeal', methods=['GET', 'POST'])
def create_meal():
    import calendar as cd
    import datetime

    if "choose_dinner" in request.form:
        dinner_id = request.form.get('choose_dinner')
        # incoming_date = request.form.get('date')

        converted_date = dinner_id.strip('][').split(', ')
        inc_dinner_id = int(converted_date[0])
        inc_year = int(converted_date[1])
        inc_month = int(converted_date[2])
        inc_day = int(converted_date[3])
        meal_date = datetime.datetime(inc_year, inc_month, inc_day)

        meal = Meal(date=meal_date, dinner_id=inc_dinner_id)
        session.add(meal)
        session.commit()
        session.close()
        return render_template(url_for('calendarroute.show_calendar'))
    else:
        incoming_date = request.form.get("add_dinner")
        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        dinners = []
        dinners.append(session.query(Dinner).all())
        session.close()
        print(dinners[0][1].title)
        # print(dinners)
        # current_date_time = datetime.datetime(inc_year, inc_month, inc_day)
        # print(str(inc_year) + ' ' + str(inc_month) + ' ' + str(inc_day))
        # print(current_date_time)
        return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day,
                               dinners=dinners)


@calendarroute.route('/createDinner', methods=['GET', 'POST'])
def create_dinner():
    if 'dinner_title' in request.form:
        dinner_title = request.form.get('dinner_title')
        user_id = request.form.get('user_id')
        group_id = request.form.get('group_id')
        # dinner_image = request.form.get('dinner_image')
        dinner_image = request.files['dinner_image'].read()
        # print(dinner_image)

        dinner = Dinner(title=dinner_title, image=dinner_image, user_id=user_id, group_id=group_id)
        session.add(dinner)
        session.commit()
        session.close()
        return render_template('createDinner.html')
    else:
        return render_template('createDinner.html')


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
