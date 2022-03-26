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
    elif "add_dinner" in request.form:
        incoming_date = request.form.get("add_dinner")
        converted_date = incoming_date.strip('][').split(', ')
        inc_year = int(converted_date[0])
        inc_month = int(converted_date[1])
        inc_day = int(converted_date[2])
        return render_template('dinner.html')

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
