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
import datetime
import isoweek
import queries


def day_strings():
    days_of_week = {"Monday": "Mandag",
                    "Tuesday": "Tirsdag",
                    "Wednesday": "Onsdag",
                    "Thursday": "Torsdag",
                    "Friday": "Fredag",
                    "Saturday": "Lørdag",
                    "Sunday": "Søndag"}
    return days_of_week


def month_strings():
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
    #group = session.query(Group).filter_by(name=group_name).first()
    group = queries.get_group_with_group_name(group_name)
    return group


def get_group_name(group_id):
    #group_name = session.query(Group).filter_by(id=group_id).first().name
    group_name = queries.get_group_with_group_id(group_id).name
    return group_name


def get_year_and_week_number(incoming_date):
    if type(incoming_date) is str:
        tmp = incoming_date.strip('][').split(', ')
        incoming_date = tmp
    incoming_year = int(incoming_date[0])
    incoming_week_number = int(incoming_date[1])
    return incoming_year, incoming_week_number


def delete_meal(incoming_date):
    converted_date = incoming_date.strip('][').split(', ')
    meal_id = int(converted_date[0])
    incoming_year = int(converted_date[1])
    incoming_week_number = int(converted_date[2])
    queries.delete_meal_with_id(meal_id)
    '''session.query(Meal).filter_by(id=meal_id).delete()
    session.commit()
    session.close()'''
    return incoming_year, incoming_week_number


def interact_with_calendar(request):
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
        '''session.query(Meal).filter_by(id=meal_id).delete()
        session.commit()'''
    elif 'set_portion' in request.form:
        incoming_date = request.form.get("mayGodGuideMeTowardTheLight")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[1])
        incoming_week_number = int(converted_date[2])
        meal_id = int(converted_date[0])
        new_portion = request.form.get("set_portion")
        queries.portion(meal_id, new_portion)
        '''meal = session.query(Meal).filter(Meal.id == meal_id).first()
        meal.portions = new_portion
        session.commit()'''
    elif 'add_portion' in request.form:
        incoming_date = request.form.get("mayGodGuideMeTowardTheLight")
        converted_date = incoming_date.strip('][').split(', ')
        incoming_year = int(converted_date[1])
        incoming_week_number = int(converted_date[2])
        meal_id = int(converted_date[0])
        new_portion = request.form.get("add_portion")
        queries.portion(meal_id, new_portion)
        '''meal = session.query(Meal).filter(Meal.id == meal_id).first()
        meal.portions = new_portion
        session.commit()'''
    elif 'remove_portion' in request.form:
        incoming_date = request.form.get("mayGodGuideMeTowardTheLight")
        converted_date = incoming_date.strip('][').split(', ')
        meal_id = int(converted_date[0])
        new_portion = request.form.get("remove_portion")
        queries.portion(meal_id, new_portion)
        '''meal = session.query(Meal).filter(Meal.id == meal_id).first()
        meal.portions = new_portion
        session.commit()'''

    elif request.args.get('create_meal_year') and request.args.get('create_meal_week_number'):
        incoming_date = [request.args.get('create_meal_year'), request.args.get('create_meal_week_number')]
        # print(incoming_date)
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
    current_date = datetime.date.today()
    days = ['1', '2', '3', '4', '5', '6', '0']
    d = None

    if incoming_week_number and incoming_year:
        d = str(incoming_year) + "-W" + str(incoming_week_number)
    else:
        d = "2022-W" + str(current_date.isocalendar().week)

    days_to_cal = []
    print(d)
    for i in days:
        days_to_cal.append(datetime.datetime.strptime(d + '-' + i, "%Y-W%W-%w"))

    for day in days_to_cal:
        print(day)

    year_to_cal = None
    if incoming_year:
        year_to_cal = incoming_year
    else:
        year_to_cal = current_date.year

    print(year_to_cal)

    week_number_to_cal = None
    if incoming_week_number is not None:
        week_number_to_cal = incoming_week_number
    else:
        week_number_to_cal = current_date.isocalendar().week
    print(week_number_to_cal)

    return days_to_cal, year_to_cal, week_number_to_cal


def get_meals(days_to_cal, group_id):
    meals = []
    for i in days_to_cal:
        if group_id:
            '''meals.append(
                session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(
                    Meal.group_id == group_id).filter(Meal.date == i.date()).first())'''
            meals.append(queries.get_meal_joined_with_dinner_with_group_id(group_id, i))
            #session.close()
        else:
            meals.append(queries.get_meal_joined_with_dinner_without_group_id(i))
            '''meals.append(
                session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(Meal.date == i).first())
            session.close()'''
    return meals


def get_dinners(meals):
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
    '''user_group_role = session.query(User_group_role).filter(User_group_role.group_id == group_id,
                                                            User_group_role.user_id == current_user.id).first()
    session.close()'''
    user_group_role = queries.get_user_group_role(current_user.id, group_id)
    session.close()
    return user_group_role


def get_current_user_role(group_id):
    '''current_user_role = session.query(User_group_role).filter(User_group_role.user_id == current_user.id,
                                                              User_group_role.group_id == group_id).first()
    session.close()'''
    current_user_role = queries.get_current_user_role_with_group_id(current_user, group_id)
    session.close()
    return current_user_role


def choose_dinner(request):
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
    #session.add(meal)
    #session.commit()
    queries.create_meal(meal)
    session.close()

    return inc_year, week_number, group_id


def add_dinner(request):
    incoming_date = request.form.get("add_dinner")
    converted_date = incoming_date.strip('][').split(', ')
    inc_year = int(converted_date[0])
    inc_month = int(converted_date[1])
    inc_day = int(converted_date[2])
    group_id = int(converted_date[3])
    #dinners = session.query(Dinner).filter_by(group_id=group_id).all()
    dinners = queries.get_dinners_by_group(group_id)
    session.close()

    conv_dinners = []
    for dinner in dinners:
        # print(dinner)
        did = dinner.id
        title = dinner.title
        dimage = base64.b64encode(dinner.image).decode("utf-8")
        conv_dinners.append([did, title, dimage])

    return inc_year, inc_month, inc_day, conv_dinners, group_id


def create_dinner(current_user, group_id):
    dinner_title = request.form.get('dinner-name')
    user_id = current_user.id
    dinner_image = request.files['dinner_image'].read()

    dinner = Dinner(title=dinner_title, image=dinner_image, user_id=user_id, group_id=group_id)
    #session.add(dinner)
    #session.commit()
    queries.create_dinner(dinner)
    session.close()

    return dinner


def get_detailed_dinner(current_user, dinner_id, group_id):
    '''current_user_role = session.query(User_group_role).filter(
        User_group_role.user_id == current_user.id,
        User_group_role.group_id == group_id).first()'''
    current_user_role = queries.get_current_user_role_with_group_id(current_user, group_id)

    def decode_image(image):
        if image is not None:
            picture = b64encode(image).decode("utf-8")
        else:
            picture = ""
        return picture

    #dinner = session.query(Dinner).filter(Dinner.id == dinner_id).first()
    dinner = queries.get_dinner_by_id(dinner_id)

    #recipe = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(desc(Recipe.version)).first()
    recipe = queries.get_recipe_with_dinner_id(dinner_id)

    image = b64encode(dinner.image).decode("utf-8")

    user = current_user
    if user.image is not None:
        image2 = b64encode(user.image).decode("utf-8")
    else:
        image2 = ""

    # kommentarer til middag
    #comments = session.query(Comment).filter(Comment.dinner_id == dinner_id).all()
    comments = queries.get_comments_by_dinner_id(dinner_id)

    # finne user som har kommentert hver kommentar
    comments_users = list()
    for comment in comments:
        comments_users.append(queries.get_user_by_id(comment.user_id))
        #comments_users.append(session.query(User).filter(User.id == comment.user_id).first())

    # finne ingredienser til oppskrift
    '''ingredients_recipe = session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()'''
    ingredients_recipe = queries.get_ingredients_by_recipe_id(recipe)
    session.close()

    # finne mengder til ingredienser
    '''amounts_recipe = session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()'''
    amounts_recipe = queries.get_amounts_by_recipe_id(recipe)
    session.close()

    # finne måleenheter for ingredienser
    '''measurements_recipe = session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()'''
    measurements_recipe = queries.get_measurements_by_recipe_id(recipe)
    session.close()

    return dinner, current_user_role, recipe, image, ingredients_recipe, amounts_recipe, measurements_recipe, comments, comments_users, image2, decode_image


def get_shopping_list(group_id):
    today = date.today()
    current_user_role = queries.get_user_group_role(current_user.id, group_id)

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

    if "complete" in request.form:
        price = request.form.get("price")
        week_number = request.form.get("week_number")
        year = request.form.get("year")
        incoming_date = request.form.get("shopping_list_date")
        new_date = date.fromisoformat(incoming_date)
        shopping_list = Shopping_list(date=new_date, price=price, week_number=week_number, year=year, group_id=group_id)
        # session.add(shopping_list)
        # session.commit()
        queries.create_shopping_list(shopping_list)

    if "undo_purchase" in request.form:
        queries.undo_shopping_list(group_id, request.form.get("year"), request.form.get("week_number"))

    weekday = new_date.weekday()
    monday = new_date - timedelta(days=weekday)
    sunday = new_date + timedelta(6 - weekday)

    week_number = datetime(new_date.year, new_date.month, new_date.day).isocalendar()[1]
    headings = ("Ingrediens", "mengde", "Enhet")

    data = queries.get_shopping_list_data(group_id, monday, sunday)

    shopping_list = queries.get_shopping_list_object(group_id, new_date.year, week_number)

    return headings, data, week_number, add_days, subtract_days, new_date


def comment_post(request, dinner_id, group_id):
    user_id = current_user.id

    if "comment" in request.form:
        text = request.form.get("comment")
    if "dinner_id" in request.form:
        dinner_id = request.form.get("dinner_id")
    if "group_id" in request.form:
        group_id = request.form.get("group_id")
        comment = Comment(user_id=user_id, dinner_id=dinner_id, text=text)
        #session.add(comment)
        #session.commit()
        queries.create_comment(comment)
        session.close()
        # Edit Comment
    if "editBtn" in request.form:
        print("jeg er i edit statement =)")
        dinner_id = request.form.get("dinner_id2")
        group_id = request.form.get("group_id2")
        comment_id = request.form.get("comment_id")
        updated_text = request.form.get("updated_text")

        # Her må tekst fra Rediger kommentar legges inn
        #copy_comment_to_edit_comment = session.query(Comment).filter(Comment.id == comment_id).first()
        copy_comment_to_edit_comment = queries.get_comment_by_id(comment_id)

        copy_data_to_edit_comment = Edited_comment(comment_id=copy_comment_to_edit_comment.id,
                                                   text=copy_comment_to_edit_comment.text)

        #session.add(copy_data_to_edit_comment)
        queries.create_edited_comment()

        session.flush()

        # update text in comment

        #newcomment = session.query(Comment).filter(Comment.id == comment_id).first()
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

        #delete_comment_edit = session.query(Edited_comment).filter(Edited_comment.comment_id == comment_id).all()
        delete_comment_edit = queries.get_edited_comments_by_comment_id(comment_id)

        for i in delete_comment_edit:
            session.delete(i)
            session.commit()

        '''delete_comment = session.query(Comment).filter(Comment.id == comment_id).first()

        print(delete_comment)

        session.delete(delete_comment)

        session.commit()'''
        queries.delete_comment_by_id(comment_id)
