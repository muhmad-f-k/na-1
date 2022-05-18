from flask_login import login_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect
from base64 import b64encode
from db.modul import *
from flask_login import current_user
import routes.calendar_methods as calendar_methods
from datetime import date, timedelta, datetime
import queries

calendarroute = Blueprint('calendarroute', __name__)


@calendarroute.route('/calendar')
def show_calendar():
    """ Render calendar with dinners belonging to either the restaurant's dinner or the group of your choice,
     it also allows users to add or remove dinners, and navigate between weeks"""
    def add_portions(portion):
        portion += 1
        return portion

    def subtract_portions(portion):
        portion -= 1
        return portion

    if request.args.get('group_name'):
        group_name = request.args.get('group_name')
        group_id = calendar_methods.get_group(group_name).id
    else:
        group_name = 'Resturant Matmons'
        group_id = calendar_methods.get_group(group_name).id

    days_of_week = calendar_methods.day_strings()
    incoming_year, incoming_week_number = calendar_methods.interact_with_calendar(request)
    days_to_cal, year_to_cal, week_number_to_cal = calendar_methods.get_days_and_week_and_year(incoming_week_number,
                                                                                               incoming_year)
    meals = calendar_methods.get_meals(days_to_cal, group_id)
    dinners = calendar_methods.get_dinners(meals)

    if current_user.is_authenticated:
        user_group_role = calendar_methods.get_user_role(group_id)
    else:
        user_group_role = None

    return render_template('groups/calendar.html', days_of_week=days_of_week, days_to_cal=days_to_cal,
                           year_to_cal=int(year_to_cal), week_number_to_cal=int(week_number_to_cal),
                           group_name=group_name, user_group_role=user_group_role,
                           group_id=group_id, dinners=dinners, meals=meals, add_portions=add_portions,
                           subtract_portions=subtract_portions)

@calendarroute.route('/calendar', methods=['POST'])
def show_calendar_post():
    """This method is called when the user navigates betwwen calendar's
    weeks in order to show the correct week and it's dinners"""
    def add_portions(portion):
        portion += 1
        return portion

    def subtract_portions(portion):
        portion -= 1
        return portion

    if request.args.get('group_name'):
        group_name = request.args.get('group_name')
        group_id = calendar_methods.get_group(group_name).id
    else:
        group_name = 'Resturant Matmons'
        group_id = calendar_methods.get_group(group_name).id

    days_of_week = calendar_methods.day_strings()
    incoming_year, incoming_week_number = calendar_methods.interact_with_calendar(request)
    days_to_cal, year_to_cal, week_number_to_cal = calendar_methods.get_days_and_week_and_year(incoming_week_number,
                                                                                               incoming_year)
    meals = calendar_methods.get_meals(days_to_cal, group_id)
    dinners = calendar_methods.get_dinners(meals)

    if current_user.is_authenticated:
        user_group_role = calendar_methods.get_user_role(group_id)
    else:
        user_group_role = None

    return render_template('groups/calendar.html', days_of_week=days_of_week, days_to_cal=days_to_cal,
                           year_to_cal=int(year_to_cal), week_number_to_cal=int(week_number_to_cal),
                           group_name=group_name, user_group_role=user_group_role,
                           group_id=group_id, dinners=dinners, meals=meals, add_portions=add_portions,
                           subtract_portions=subtract_portions)


@calendarroute.route('/createMeal')
def create_meal():
    """Render page that shows all dinners belonging to current group, and lets user add them to that group's calendar"""
    return render_template('groups/add_dinner_to_calendar.html')


@calendarroute.route('/createMeal', methods=['POST'])
def create_meal_post():
    """This method receives the chosen dinner and adds it to the current group's calendar"""
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
    """Render the page that allows user to create a dinner for current group"""
    current_user_role = calendar_methods.get_current_user_role(group_id)
    return render_template('dinners/create_dinner.html', current_user_role=current_user_role)


@calendarroute.route('/createDinner/<group_id>', methods=['POST'])
def create_dinner_post(group_id):
    """This method receives values from the dinner creation page and creates a new dinner"""
    dinner = calendar_methods.create_dinner(current_user, group_id)
    #session.close()
    return redirect(url_for(
        "recipe_route.create_recipe", dinner_id=dinner.id))


@calendarroute.route('/show_group_dinners/<group_id>')
def show_group_dinners(group_id):
    """Render page that shows all dinner belonging to that group"""
    dinners = session.query(Dinner).filter(Dinner.group_id == group_id).all()

    def decode_image(image):
        picture = b64encode(image).decode("utf-8")
        return picture

    session.close()
    return render_template("dinners.html", dinners=dinners, group_id=group_id, decode_image=decode_image)


@calendarroute.route('/show_dinner/<dinner_id>/<group_id>')
def show_dinner(dinner_id, group_id):
    """Render page that shows ingredients, recipe, comments and picture belonging to one dinner"""
    dinner, current_user_role, recipe, image, ingredients_recipe, amounts_recipe, measurements_recipe, comments, comments_users, image2, decode_image = calendar_methods.get_detailed_dinner(current_user, dinner_id, group_id)
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


@calendarroute.route('/shopping_list/<group_id>', methods=['GET', 'POST'])
def show_shopping_list(group_id):
    """Render page that shows the shopping list of ingredients of dinners in a chosen period of time"""
    #Henter dagens dato og henter brukeren og hans rolle i gruppen
    today = date.today()
    current_user_role = queries.get_user_group_role(current_user.id, group_id)

    #Metoder som kjøres i shopping_list.html som legger til og trekker fra dagens dato med 7 dager
    def add_days(date):
        date += timedelta(days=7)
        return date

    def subtract_days(date):
        date -= timedelta(days=7)
        return date

    #Går til neste eller forrige handleliste
    if "next_week" in request.form:
        incoming_date = request.form.get("next_week")
        new_date = date.fromisoformat(incoming_date)

    elif "prev_week" in request.form:
        incoming_date = request.form.get("prev_week")
        new_date = date.fromisoformat(incoming_date)

    #Når brukeren først trykker inn på handlelisten vil nåværernde ukes handleliste vises
    else:
        new_date = today

    #Lager et shopping_list object med prisen brukeren legger inn og lagrer det i databasen
    if "complete" in request.form:
        price = request.form.get("price")
        week_number = request.form.get("week_number")
        year = request.form.get("year")
        incoming_date = request.form.get("shopping_list_date")
        new_date = date.fromisoformat(incoming_date)
        shopping_list = Shopping_list(date=new_date, price=price, week_number=week_number, year=year, group_id=group_id)
        session.add(shopping_list)
        session.commit()

    #Sletter handleliste-objektet slik at brukeren kan legge inn ny pris
    if "undo_purchase" in request.form:
        queries.undo_shopping_list(group_id, request.form.get("year"), request.form.get("week_number"))

    #Finner mandag og søndag ved hjelp av dagens dato slik at man kan finne ingredienser til den spesifikke uken
    weekday = new_date.weekday()
    monday = new_date - timedelta(days=weekday)
    sunday = new_date + timedelta(6 - weekday)

    week_number = datetime(new_date.year, new_date.month, new_date.day).isocalendar()[1]
    headings = ("Ingrediens", "mengde", "Enhet")

    #Henter alle ingredienser som trengs for den spesifikke uken
    data = queries.get_shopping_list_data(group_id, monday, sunday)

    #Sjekker om handlelisten for den spesifikke uken er handlet. Returnerer denne null så er ikke ukens handleliste handlet.
    shopping_list = queries.get_shopping_list_object(group_id, new_date.year, week_number)

    return render_template('groups/shopping_list.html', headings=headings, data=data, group_id=group_id,
                           week_number=week_number, add_days=add_days, subtract_days=subtract_days,
                           new_date=new_date, year=new_date.year, shopping_list=shopping_list,
                           current_user_role=current_user_role)

@calendarroute.route('/show_dinner/<dinner_id>/<group_id>', methods=['POST'])
@login_required
def comment_post(dinner_id, group_id):
    """This method takes in values from a dinner's info page and creates/edits or deletes a comment"""
    user_id = current_user.id

    if "comment" in request.form:
        text = request.form.get("comment")
    if "dinner_id" in request.form:
        dinner_id = request.form.get("dinner_id")
    if "group_id" in request.form:
        group_id = request.form.get("group_id")
        comment = Comment(user_id=user_id, dinner_id=dinner_id, text=text)
        session.add(comment)
        session.commit()
        session.close()
        # Edit Comment
    if "editBtn" in request.form:
        print("jeg er i edit statement =)")
        dinner_id = request.form.get("dinner_id2")
        group_id = request.form.get("group_id2")
        comment_id = request.form.get("comment_id")
        updated_text = request.form.get("updated_text")

        # Her må tekst fra Rediger kommentar legges inn
        copy_comment_to_edit_comment = session.query(Comment).filter(Comment.id == comment_id).first()

        copy_data_to_edit_comment = Edited_comment(comment_id=copy_comment_to_edit_comment.id,
                                                   text=copy_comment_to_edit_comment.text)

        session.add(copy_data_to_edit_comment)

        session.flush()

        # update text in comment

        newcomment = session.query(Comment).filter(Comment.id == comment_id).first()

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

        delete_comment_edit = session.query(Edited_comment).filter(Edited_comment.comment_id == comment_id).all()

        for i in delete_comment_edit:
            session.delete(i)
            session.commit()

        delete_comment = session.query(Comment).filter(Comment.id == comment_id).first()

        print(delete_comment)

        session.delete(delete_comment)

        session.commit()
    return redirect(url_for("calendarroute.show_dinner", dinner_id=dinner_id, group_id=group_id))