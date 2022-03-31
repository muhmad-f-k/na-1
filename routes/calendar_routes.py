import base64
import io

from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, login_required, current_user, logout_user
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

    group_id = None
    group_name = None
    if request.args.get('group_id'):
        group_id = int(request.args.get('group_id'))
        group_name = session.query(Group).filter_by(id=group_id).first().name
        print(group_name)
    else:
        group_name = 'Restaurant'
        print(group_name)
        pass


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
        # print(request.form.get('delete_meal'))
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

    # dinner = meals[0][1]
    # image = base64.b64encode(dinner.image).decode("utf-8")

    return render_template('calendar.html',
                           days_of_week=days_of_week, full_month=full_month, year=year, month=month,
                           month_name=month_name, dinners=dinners, meals=meals, group_id=group_id, group_name=group_name)


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
        group_id = int(converted_date[4])
        meal_date = datetime.datetime(inc_year, inc_month, inc_day)

        meal = Meal(date=meal_date, dinner_id=inc_dinner_id, group_id=group_id)
        session.add(meal)
        session.commit()
        session.close()
        #return render_template(url_for('calendarroute.show_calendar'))
        return redirect(url_for('calendarroute.show_calendar',
                                create_meal_year=inc_year, create_meal_month=inc_month, group_id=group_id))
    else:
        incoming_date = request.form.get("add_dinner")
        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        group_id = int(converted_date[3])
        # dinners = []
        # dinners.append(session.query(Dinner).all())
        dinners = session.query(Dinner).filter_by(group_id=group_id).all()
        session.close()
        # print(dinners)

        conv_dinners = []
        for dinner in dinners:
            # print(dinner)
            did = dinner.id
            title = dinner.title
            dimage = base64.b64encode(dinner.image).decode("utf-8")
            conv_dinners.append([did, title, dimage])

        # return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day, dinners=dinners)
        return render_template('createMeal.html', inc_year=inc_year, inc_month=inc_month, inc_day=inc_day,
                               dinners=conv_dinners, group_id=group_id)


@calendarroute.route('/createDinner', methods=['GET', 'POST'])
def create_dinner():
    if 'dinner_title' in request.form:
        dinner_title = request.form.get('dinner_title')
        # user_id = request.form.get('user_id')

        # group_id = request.form.get('group_id')
        group_id = int(request.form.get('group_id'))
        # dinner_image = request.form.get('dinner_image')

        dinner_image = request.files['dinner_image'].read()
        # print(dinner_image)

        dinner = Dinner(title=dinner_title, image=dinner_image, user_id=current_user.id, group_id=group_id)
        session.add(dinner)
        session.commit()
        session.close()
        return render_template('createDinner.html')
    else:
        group_id = int(request.args.get('group_id'))
        print(group_id)
        return render_template('createDinner.html', group_id=group_id)


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
