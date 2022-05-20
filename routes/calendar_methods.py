import base64
from flask import request
from sqlalchemy import desc
from base64 import b64encode
from db.modul import *
from flask_login import current_user
from datetime import date, timedelta, datetime
import datetime
import isoweek
import queries


def day_strings():
    """This method returns the norwegian translation of all weekdays"""
    days_of_week = {"Monday": "Mandag",
                    "Tuesday": "Tirsdag",
                    "Wednesday": "Onsdag",
                    "Thursday": "Torsdag",
                    "Friday": "Fredag",
                    "Saturday": "Lørdag",
                    "Sunday": "Søndag"}
    return days_of_week


def month_strings():
    """This method returns the norwegian translation of all months of the year"""
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
    return months_of_year


def get_group(group_name):
    """This method returns the group with the correct name"""
    group = queries.get_group_with_group_name(group_name)
    return group


def get_group_name(group_id):
    """This method returns the group's name with the correct id"""
    group_name = queries.get_group_with_group_id(group_id).name
    return group_name


def get_year_and_week_number(incoming_date):
    """This method returns the year and week number from the provided date"""
    if type(incoming_date) is str:
        tmp = incoming_date.strip('][').split(', ')
        incoming_date = tmp
    incoming_year = int(incoming_date[0])
    incoming_week_number = int(incoming_date[1])
    return incoming_year, incoming_week_number


def delete_meal(incoming_date):
    """This method deletes the meal connecting a dinner to a date, using the provided date"""
    converted_date = incoming_date.strip('][').split(', ')
    meal_id = int(converted_date[0])
    incoming_year = int(converted_date[1])
    incoming_week_number = int(converted_date[2])
    queries.delete_meal_with_id(meal_id)
    return incoming_year, incoming_week_number


def interact_with_calendar(request):
    """This method decides what happens when the user uses the calendar, either navigate to next/previous week,
    create/delete meal or add/remove portions from dinners.
    It also only allows user to navigate 2000 years back in time"""
    incoming_week_number = None
    incoming_year = None

    if "next_week" in request.form:
        incoming_date = request.form.get("next_week")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[0])
        incoming_week_number = int(converted_date[1])
    elif "prev_week" in request.form:
        incoming_date = request.form.get("prev_week")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[0])
        incoming_week_number = int(converted_date[1])
    elif 'delete_meal' in request.form:
        incoming_date = request.form.get("delete_meal")
        converted_date = incoming_date.strip('][').split(', ')
        meal_id = int(converted_date[0])
        incoming_year = int(converted_date[1])
        incoming_week_number = int(converted_date[2])
        queries.delete_meal_with_id(meal_id)
    elif 'set_portion' in request.form:
        incoming_date = request.form.get("list_of_data")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[1])
        incoming_week_number = int(converted_date[2])
        meal_id = int(converted_date[0])
        new_portion = request.form.get("set_portion")
        if int(new_portion) < 1:
            new_portion = 1
        queries.portion(meal_id, new_portion)
    elif 'add_portion' in request.form:
        incoming_date = request.form.get("list_of_data")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[1])
        incoming_week_number = int(converted_date[2])
        meal_id = int(converted_date[0])
        new_portion = request.form.get("add_portion")
        queries.portion(meal_id, new_portion)
    elif 'remove_portion' in request.form:
        incoming_date = request.form.get("list_of_data")
        converted_date = incoming_date.strip('][').split(', ')
        meal_id = int(converted_date[0])
        new_portion = request.form.get("remove_portion")
        if int(new_portion) < 1:
            new_portion = 1
        queries.portion(meal_id, new_portion)

    elif request.args.get('create_meal_year') and request.args.get('create_meal_week_number'):
        incoming_date = [request.args.get('create_meal_year'), request.args.get('create_meal_week_number')]
        incoming_year = int(incoming_date[0])
        incoming_week_number = int(incoming_date[1])

    if incoming_week_number is not None and incoming_year is not None:
        current_date = datetime.datetime(int(incoming_year), 1, 1)
        last_week_number = str(isoweek.Week.last_week_of_year(current_date.year).week)

        if int(incoming_week_number) > int(last_week_number):
            incoming_week_number = str(1)
            tmp = str(int(incoming_year) + 1)
            incoming_year = tmp
        elif int(incoming_week_number) < 1:
            incoming_week_number = str(isoweek.Week.last_week_of_year(current_date.year - 1).week)
            tmp = str(int(incoming_year) - 1)
            incoming_year = tmp

        if int(incoming_year) < 1:
            incoming_year = '0001'
        elif int(incoming_year) < 10:
            tmp = '000' + incoming_year
            incoming_year = tmp
        elif int(incoming_year) < 100:
            tmp = '00' + incoming_year
            incoming_year = tmp
        elif int(incoming_year) < 1000:
            tmp = '0' + incoming_year
            incoming_year = tmp

    return incoming_year, incoming_week_number


def get_days_and_week_and_year(incoming_week_number, incoming_year):
    """This method returns all day dates of a week with the provided week number and year"""
    current_date = datetime.date.today()
    days = ['1', '2', '3', '4', '5', '6', '0']

    if incoming_week_number and incoming_year:
        d = str(incoming_year) + "-W" + str(incoming_week_number)
    else:
        d = "2022-W" + str(current_date.isocalendar().week)

    days_to_cal = []
    for i in days:
        days_to_cal.append(datetime.datetime.strptime(d + '-' + i, "%Y-W%W-%w"))

    if incoming_year:
        year_to_cal = incoming_year
    else:
        year_to_cal = current_date.year

    if incoming_week_number is not None:
        week_number_to_cal = incoming_week_number
    else:
        week_number_to_cal = current_date.isocalendar().week

    return days_to_cal, year_to_cal, week_number_to_cal


def get_meals(days_to_cal, group_id):
    """This method returns all dinners for a week belonging to a specific group,
    using the provided dates and group id"""
    meals = []
    for i in days_to_cal:
        if group_id:
            meals.append(queries.get_meal_joined_with_dinner_with_group_id(group_id, i))
        else:
            meals.append(queries.get_meal_joined_with_dinner_without_group_id(i))
    return meals


def get_dinners(meals):
    """This method returns all dinners belonging to the provided meals"""
    dinners = []
    for n in meals:
        if n:
            dinner = n[1]
            title = dinner.title
            dimage = base64.b64encode(dinner.image).decode("utf-8")
            dinners.append([title, dimage])
        else:
            dinners.append(n)

    return dinners


def get_user_role(group_id):
    """This method returns the user's role within the provided group"""
    user_group_role = queries.get_user_group_role(current_user.id, group_id)
    session.close()
    return user_group_role


def get_current_user_role(group_id):
    """This method returns the current user's role within the provided group"""
    current_user_role = queries.get_current_user_role_with_group_id(current_user, group_id)
    session.close()
    return current_user_role


def choose_dinner(request):
    """This method creates a new meal and assigns a dinner to it,
     and returns the year, week number and group id of that meal"""
    dinner_id = request.form.get('choose_dinner')

    converted_date = dinner_id.strip('][').split(', ')
    inc_dinner_id = int(converted_date[0])
    inc_year = int(converted_date[1])
    inc_month = int(converted_date[2])
    inc_day = int(converted_date[3])
    group_id = int(converted_date[4])
    meal_date = datetime.datetime(inc_year, inc_month, inc_day)
    week_number = meal_date.isocalendar().week
    meal_portions = session.query(Recipe).filter(
        Recipe.dinner_id == inc_dinner_id).order_by(desc(Recipe.version)).first()

    meal = Meal(date=meal_date, portions=meal_portions.portions, dinner_id=inc_dinner_id, group_id=group_id)
    queries.create_meal(meal)
    session.close()

    return inc_year, week_number, group_id


def add_dinner(request):
    """This method returns all dinners belogning to current group so user can select on for a meal,
    including the year, month, day and group id for that meal"""
    incoming_date = request.form.get("add_dinner")
    converted_date = incoming_date.strip('][').split(', ')
    inc_year = int(converted_date[0])
    inc_month = int(converted_date[1])
    inc_day = int(converted_date[2])
    group_id = int(converted_date[3])
    dinners = queries.get_dinners_by_group(group_id)
    session.close()

    conv_dinners = []
    for dinner in dinners:
        did = dinner.id
        title = dinner.title
        dimage = base64.b64encode(dinner.image).decode("utf-8")
        conv_dinners.append([did, title, dimage])

    return inc_year, inc_month, inc_day, conv_dinners, group_id


def create_dinner(current_user, group_id):
    """This method creates and returns a dinner"""
    dinner_title = request.form.get('dinner-name')
    user_id = current_user.id
    dinner_image = request.files['dinner_image'].read()

    dinner = Dinner(title=dinner_title, image=dinner_image, user_id=user_id, group_id=group_id)
    queries.create_dinner(dinner)
    #session.close()

    return dinner


def get_detailed_dinner(current_user, dinner_id, group_id):
    """This method returns all information about a dinner,
    including the current user's role, which decides if hte user is allowed to change the dinner"""
    if current_user.is_authenticated:
        current_user_role = queries.get_current_user_role_with_group_id(current_user, group_id)
    else:
        current_user_role = None

    def decode_image(image):
        if image is not None:
            picture = b64encode(image).decode("utf-8")
        else:
            picture = ""
        return picture

    dinner = queries.get_dinner_by_id(dinner_id)

    recipe = queries.get_recipe_with_dinner_id(dinner_id)

    image = b64encode(dinner.image).decode("utf-8")

    if current_user.is_authenticated:
        user = current_user
        if user.image is not None:
            image2 = b64encode(user.image).decode("utf-8")
        else:
            image2 = ""
    else:
        image2 = ""

    # kommentarer til middag
    comments = queries.get_comments_by_dinner_id(dinner_id)

    # finne user som har kommentert hver kommentar
    comments_users = list()
    for comment in comments:
        comments_users.append(queries.get_user_by_id(comment.user_id))

    # finne ingredienser til oppskrift
    ingredients_recipe = queries.get_ingredients_by_recipe_id(recipe)
    session.close()

    # finne mengder til ingredienser
    amounts_recipe = queries.get_amounts_by_recipe_id(recipe)
    session.close()

    # finne måleenheter for ingredienser
    measurements_recipe = queries.get_measurements_by_recipe_id(recipe)
    session.close()

    return dinner, current_user_role, recipe, image, ingredients_recipe, amounts_recipe, measurements_recipe, comments, comments_users, image2, decode_image


def comment_post(request, dinner_id, group_id):
    """This method takes in values from a dinner's info page and creates/edits or deletes a comment"""
    user_id = current_user.id

    if "comment" in request.form:
        text = request.form.get("comment")
    if "dinner_id" in request.form:
        dinner_id = request.form.get("dinner_id")
    if "group_id" in request.form:
        group_id = request.form.get("group_id")
        comment = Comment(user_id=user_id, dinner_id=dinner_id, text=text)
        queries.create_comment(comment)
        session.close()
        # Edit Comment
    if "editBtn" in request.form:
        dinner_id = request.form.get("dinner_id2")
        group_id = request.form.get("group_id2")
        comment_id = request.form.get("comment_id")
        updated_text = request.form.get("updated_text")

        # Her må tekst fra Rediger kommentar legges inn
        copy_comment_to_edit_comment = queries.get_comment_by_id(comment_id)

        copy_data_to_edit_comment = Edited_comment(comment_id=copy_comment_to_edit_comment.id,
                                                   text=copy_comment_to_edit_comment.text)

        queries.create_edited_comment()

        session.flush()

        # update text in comment

        newcomment = queries.get_comment_by_id(comment_id)

        newcomment.text = updated_text
        session.commit()

        # delete Comment
    if "delBtn" in request.form:
        dinner_id = request.form.get("dinner_id2")
        group_id = request.form.get("group_id2")
        comment_id = request.form.get("comment_id")
        # //////////////////////////////////////////////////////////////////////////
        # Denne må vi huske på å legge inn når vi har modul med Deleted-comment <3
        # ///////////////////////////////////////////////////////////////////////////

        # copy_comment_to_deleted_comment = session.query(Comment).filter(Comment.id == comment_id).first()
        #
        # copy_data_to_deleted_comment = Deleted_comment(comment_id=copy_comment_to_edit_comment.id,
        #                                                text=copy_comment_to_edit_comment.text)
        #
        # session.add(copy_data_to_edit_comment)
        #
        # session.flush()

        delete_comment_edit = queries.get_edited_comments_by_comment_id(comment_id)

        for i in delete_comment_edit:
            session.delete(i)
            session.commit()

        queries.delete_comment_by_id(comment_id)