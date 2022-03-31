from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

usersroute = Blueprint('usersroute', __name__)

#group = session.query(Group).filter(Group.id == 1).first()


@usersroute.route("/")
def home():
    return render_template("home.html")


@usersroute.route('/profile')
@login_required
def profile():
    name = current_user.first_name
    session.close()
    groups = session.query(Group.name).join(
        User_group_role).join(User).filter(User.id == current_user.id).all()
    session.close()

    roles = session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == current_user.id).all()
    session.close()

    return render_template('profile.html', name=name, groups=groups, roles=roles, id=current_user.id)


@usersroute.route("/login")
def login():
    return render_template("login.html")


@usersroute.route("/login", methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    user = session.query(User).filter(User.email == email).first()
    session.close()

    if user is None or not check_password_hash(user.password, password):
        flash("Sjekk din logg inn detaljer")
        return redirect(url_for("usersroute.login"))

    login_user(user)

    return redirect(url_for("usersroute.profile"))


@usersroute.route("/register")
def register():
    return render_template("register.html")


@usersroute.route("/register", methods=['POST'])
def register_post():
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    user = session.query(User).filter(User.email == email).first()
    session.close()
    if user:
        flash("Email er allerede registrert. Gå til logg inn.")
        return redirect(url_for("usersroute.login"))

    elif password != confirm_password:
        flash("Passordene stemmer ikke overens. Prøv igjen.")
        return redirect(url_for("usersroute.register"))

    else:
        new_user = User(email=email, first_name=first_name,
                        last_name=last_name, password=generate_password_hash(password, method="sha256"))
        session.add(new_user)
        session.commit()
        session.close()

    return redirect(url_for("usersroute.login"))


@usersroute.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("home.html")
