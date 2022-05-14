from base64 import b64encode
from distutils.log import error
from email.mime import image
from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import *
from sqlalchemy import func, null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

usersroute = Blueprint('usersroute', __name__)


@usersroute.route("/")
def home():
    return render_template("home.html")


@usersroute.route('/profile')
@login_required
def profile():
    user = current_user
    if user.image is not None:
        image = b64encode(user.image).decode("utf-8")
    else:
        image = ""
    session.close()
    groups = session.query(Group).join(
        User_group_role).join(User).filter(User.id == current_user.id).all()
    session.close()

    roles = session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == current_user.id).all()
    session.close()

    return render_template('users/profile.html', user=user, groups=groups, roles=roles, image=image)


@usersroute.route('/profile', methods=['POST'])
@login_required
def profile_post():
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
    if current_user.is_authenticated:
        return redirect(url_for("usersroute.profile"))
    else:
        return render_template("/users/login.html")


@usersroute.route("/login", methods=['POST'])
def login_post():
    user = session.query(User).filter(User.email == request.form.get("email").lower()).first()

    if user is None:
        flash("E-postadressen eksisterer ikke.", 'warning')
    if user:
        verify_password = user.verify_password(request.form.get("password"))
        if verify_password:
            login_user(user)
        if verify_password is not True:
            flash("Feil passord, Prøv igjen!", 'error')

    return redirect(url_for("usersroute.profile"))


@usersroute.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("usersroute.profile"))
    else:
        return render_template("/users/register.html")


@usersroute.route("/register", methods=['POST'])
def register_post():
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    user = session.query(User).filter(User.email == email.lower()).first()
    session.close()
    if user:
        flash("Email er allerede registrert. Gå til logg inn.", "info")
        return redirect(url_for("usersroute.login"))

    elif password != confirm_password:
        flash("Passordene stemmer ikke overens. Prøv igjen.", "warning")
        return redirect(url_for("usersroute.register"))

    else:
        new_user = User(email=email.lower(), first_name=first_name.lower(),
                        last_name=last_name.lower(), set_password=password)
        session.add(new_user)
        session.commit()
        session.close()
        flash("Bruker opprettet!", "success")

    return redirect(url_for("usersroute.login"))


@usersroute.route('/personvern')
def privacy():
    return render_template("/info/privacy.html")


@usersroute.route('/Vilkår_for_bruk')
def terms_of_use():
    return render_template("/info/terms_of_use.html")


@usersroute.route('/Bruksanvisning')
def instructions_for_use():
    return render_template("/info/instructions_for_use.html")


@usersroute.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("usersroute.home"))


def delete_user():
    session.query(User).filter_by(id=current_user.id).delete()
    session.commit()
    flash("Oisann! Bruker slettet :/", "info")
    return redirect(url_for("usersroute.home"))


def update_user():
    user = session.query(User).filter(User.id == current_user.id).first()
    check_email = session.query(User).filter(User.email == request.form.get("email")).first()
    find_id = session.query(User.id).filter(User.email == request.form.get("email")).first()
    # return true or false
    final_check_email = check_email.id == find_id.id
    final_check_2 = current_user.id == find_id.id

    # sjekk email

    if request.form.get("password") != request.form.get("confirm_password"):
        flash("Passordene stemmer ikke oversens. Prøv igjen!", "warning")

    if check_email and final_check_2 is not True:
        flash("E-postadressen eksisterer allerede.", "warning")

    if current_user.email != request.form.get("email") and request.form.get("password") == request.form.get(
            "confirm_password") and check_email is None:
        user.email = request.form.get("email").lower()
        session.commit()
        print("endret email")
        flash("Bruker oppdatert!", "success")

    if current_user.first_name != request.form.get("first_name") and request.form.get("password") == request.form.get(
            "confirm_password") and final_check_email is True or check_email is None:
        user.first_name = request.form.get("first_name").lower()
        session.commit()
        print("endret first name")
        flash("Bruker oppdatert!", "success")

    if current_user.last_name != request.form.get("last_name") and request.form.get("password") == request.form.get(
            "confirm_password") and final_check_email is True or check_email is None:
        user.last_name = request.form.get("last_name").lower()
        session.commit()
        print("endret last name")
        flash("Bruker oppdatert!", "success")

    if user.verify_password(request.form.get("password")) is not True and request.form.get(
            "password") == request.form.get("confirm_password") and final_check_email is True or check_email is None:
        user.set_password = request.form.get("password")
        session.commit()
        print("endret passord")
        flash("Bruker oppdatert!", "success")


def create_group():
    name = request.form.get("group-name")
    group_exist = session.query(Group).filter(Group.name == name).first()
    if group_exist is not None:
        flash("Gruppenavn er allerede tatt - Vennligst velg et annet navn", "warning")
        return redirect(url_for("usersroute.profile"))
    elif group_exist is None:
        group = Group(name=name)
        session.add(group)
        session.commit()
        session.close()

        new_group = session.query(Group).filter(Group.name == name).first()
        role = session.query(Role).filter(Role.id == 1).first()
        assoc = User_group_role(user_id=current_user.id, group_id=new_group.id, role_id=role.id)
        session.add(assoc)
        session.commit()
        session.close()
        flash("Gruppe opprettet!", "success")
        return redirect(url_for("usersroute.profile"))

    else:
        return redirect(url_for("usersroute.profile"))


def add_profile_img():
    profile_img = request.files['profile_image'].read()
    user = session.query(User).get(current_user.id)
    user.image = profile_img
    session.commit()
    session.close()
    return redirect(url_for("usersroute.home"))
