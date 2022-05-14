from base64 import b64encode
from cgi import test
from flask import Blueprint, redirect, render_template, request, url_for, flash

import queries
from db.modul import *
from queries import *
from flask_login import login_user, login_required, current_user, logout_user

usersroute = Blueprint('usersroute', __name__)


@usersroute.route("/")
def home():
    """ Render home page"""
    return render_template("home.html")


@usersroute.route('/profile')
@login_required
def profile():
    """ Render current logged in user with their picture"""
    if current_user.image is not None:
        image = b64encode(current_user.image).decode("utf-8")
    else:
        image = ""
    return render_template('users/profile.html', user=current_user, groups=get_groups_with_user_id(current_user.id), roles=get_roles_with_user_id(current_user.id), image=image)


@usersroute.route('/profile', methods=['POST'])
@login_required
def profile_post():
    """This post method calls other methods to deal with user delete own profile, update user details, create group and add user profile image."""
    if request.form.get("action_delete") == "slett_bruker":
        delete_user()
        return redirect(url_for("usersroute.home"))
    if request.form.get("action_update_user") == "oppdater":
        update_user()
        return redirect(url_for("usersroute.profile"))
    if request.form.get("action_add_group") == "opprett":
        create_group()
        return redirect(url_for("usersroute.profile"))
    if request.form.get("action_add_img") == "endre":
        add_profile_img()
        return redirect(url_for("usersroute.profile"))


@usersroute.route("/login")
def login():
    """Method render login html and deal with login if user authenticated will redirect to user profile and if not authenticated it will redirect to login page """
    if current_user.is_authenticated:
        return redirect(url_for("usersroute.profile"))
    else:
        return render_template("/users/login.html")


@usersroute.route("/login", methods=['POST'])
def login_post():
    """This login post method deal with user data and check user details - its verify password, email and if enter data correct then user will be logged in and redicret to current user profile."""
    if get_user_by_email(request.form.get("email").lower()) is None:
        flash("E-postadressen eksisterer ikke.", 'warning')
    if get_user_by_email(request.form.get("email").lower()):
        verify_password = get_user_by_email(request.form.get(
            "email").lower()).verify_password(request.form.get("password"))
        if verify_password:
            login_user(get_user_by_email(request.form.get("email").lower()))
        if verify_password is not True:
            flash("Feil passord, Prøv igjen!", 'error')

    return redirect(url_for("usersroute.profile"))


@usersroute.route("/register")
def register():
    """Register method - this render register html page and checks if user is authenticated and if user authenticated then will redirect user to profiler page"""
    if current_user.is_authenticated:
        return redirect(url_for("usersroute.profile"))
    else:
        return render_template("/users/register.html")


@usersroute.route("/register", methods=['POST'])
def register_post():
    """this is register post method, this deal with data enterd by user and after all details enterd then will redirect user to login page. """
    if get_user_by_email(request.form.get("email")):
        flash("Email er allerede registrert. Gå til logg inn.", "info")
        return redirect(url_for("usersroute.login"))

    elif request.form.get("password") != request.form.get("confirm_password"):
        flash("Passordene stemmer ikke overens. Prøv igjen.", "warning")
        return redirect(url_for("usersroute.register"))

    else:
        save_user_details(request.form.get("email").lower(), request.form.get("first_name").lower(),request.form.get("last_name").lower(),request.form.get("password"))
        flash("Bruker opprettet!", "success")

    return redirect(url_for("usersroute.login"))


@usersroute.route('/personvern')
def privacy():
    """Method renders privacy html page """
    return render_template("/info/privacy.html")


@usersroute.route('/logout')
@login_required
def logout():
    """This method log out user and redirect to home page."""
    logout_user()
    return redirect(url_for("usersroute.home"))


def delete_user():
    """this method deal with delete user profile."""
    detete_user_by_id(current_user.id)
    session.commit()
    flash("Oisann! Bruker slettet :/", "info")
    return redirect(url_for("usersroute.home"))


def update_user():
    """this method deal with user updating their profile details"""
    """Sjekker om passord stemmer overren"""
    if request.form.get("password") != request.form.get("confirm_password"):
        flash("Passordene stemmer ikke oversens. Prøv igjen!", "warning")
    """sjekker om ny email allerede registert og eies av noen andre"""
    if get_user_by_email(request.form.get("email")) and bool(current_user.id == get_user_by_email(request.form.get("email")).id) is not True:
        flash("E-postadressen eksisterer allerede.", "warning")
    """Sjekke om email taste av bruker om det samme som eksisterende email da vil den ikke commit til data - sånn slipper man å skrive over til database når det samme email"""
    if current_user.email != request.form.get("email") and request.form.get("password") == request.form.get(
            "confirm_password") and get_user_by_email(request.form.get("email")) is None:
        get_user_by_id(current_user.id).email = request.form.get(
            "email").lower()
        session.commit()
        flash("Bruker oppdatert!", "success")
    """Sjekker om første navn samme som første navn i database- vi det ikke samme så skrive inn nye første navn -sånn slipper man å skrive over til database når det samme første navn"""
    if current_user.first_name != request.form.get("first_name") and request.form.get("password") == request.form.get(
            "confirm_password") and bool(current_user.id == get_user_by_email(
                request.form.get("email")).id) is True or get_user_by_email(request.form.get("email")) is None:
        get_user_by_id(current_user.id).first_name = request.form.get(
            "first_name").lower()
        session.commit()
        print("endret first name")
        flash("Bruker oppdatert!", "success")
        """Sjekker om etter navn samme som etter navn i database- vi det ikke samme så skrive inn nye etter navn - sånn slipper man å skrive over til database når det samme etter navn"""
    if current_user.last_name != request.form.get("last_name") and request.form.get("password") == request.form.get(
            "confirm_password") and bool(current_user.id == get_user_by_email(
                request.form.get("email")).id) is True or get_user_by_email(request.form.get("email")) is None:
        get_user_by_id(current_user.id).last_name = request.form.get(
            "last_name").lower()
        session.commit()
        print("endret last name")
        flash("Bruker oppdatert!", "success")
        """Sjekker om passord samme som passord i database- vi det ikke samme så skrive inn nye passord - sånn slipper man å skrive over til database når det samme passord"""
    if get_user_by_id(current_user.id).verify_password(request.form.get("password")) is not True and request.form.get(
            "password") == request.form.get("confirm_password") and bool(current_user.id == get_user_by_email(
                request.form.get("email")).id) is True or get_user_by_email(request.form.get("email")) is None:
        get_user_by_id(
            current_user.id).set_password = request.form.get("password")
        session.commit()
        flash("Bruker oppdatert!", "success")


def create_group():
    """this method deal with create group for a user."""
    if get_group_with_group_name(request.form.get("group-name")) is not None:
        flash("Gruppenavn er allerede tatt - Vennligst velg et annet navn", "warning")
        return redirect(url_for("usersroute.profile"))
    if get_group_with_group_name(request.form.get("group-name")) is None:
        """Hvis Gruppe ikke finnes i database så legges til group table"""
        save_group_name(request.form.get("group-name"))

        """Henter admin role og legge til bruker som har oprettet gruppen."""
        role = "admin"
        save_role_group(current_user.id, get_group_with_group_name(
            request.form.get("group-name")).id, get_role_by_name(role).id)
        flash("Gruppe opprettet!", "success")
        return redirect(url_for("usersroute.profile"))

    else:
        return redirect(url_for("usersroute.profile"))


def add_profile_img():
    """this method add user profile picture to database."""
    get_user_by_id(
        current_user.id).image = request.files['profile_image'].read()
    session.commit()
    return redirect(url_for("usersroute.home"))
