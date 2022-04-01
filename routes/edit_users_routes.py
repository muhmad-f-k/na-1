
from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import session, User
from werkzeug.security import generate_password_hash
from flask_login import current_user

edituserroute = Blueprint('edituserroute', __name__)


@edituserroute.route("/update_user")
def update_user():
    return render_template("update_user.html", first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email)


@edituserroute.route("/update_user", methods=['POST'])
def update_user_post():

    user = session.query(User).get(current_user.id)
    user.first_name = request.form.get("first_name")
    user.last_name = request.form.get("last_name")
    new_password = request.form.get("password")
    new_password_confirm = request.form.get("confirm_password")

    if new_password != new_password_confirm:
        flash("Passordene stemmer ikke oversens. Prøv igjen!")
        return redirect(url_for("edituserroute.update_user"))

    else:

        if current_user.email == request.form.get("email"):
            user.password = generate_password_hash(
                new_password, method="sha256")
            flash("Bruker oppdatert!")
            session.commit()
            session.close()
            return redirect(url_for("usersroute.profile"))

        elif session.query(User).filter(User.email == request.form.get("email")):
            flash("E-posten finnes allerede, prøv på nytt.")
            return redirect(url_for("edituserroute.update_user"))

        else:
            user.email = request.form.get("email")

            user.password = generate_password_hash(
                new_password, method="sha256")
            flash("Bruker oppdatert!")
            session.commit()
            session.close()
            return redirect(url_for("usersroute.profile"))


#@edituserroute.route("/delete_user")
#def delete_user():
#    return render_template("delete_user.html", first_name=current_user.first_name, last_name=current_user.last_name)


@edituserroute.route("/profile", methods=['POST'])
def delete_user_post():
    if request.form.get("action_delete") == "slett_bruker":
        deleted_user = session.query(User).get(current_user.id)
        session.delete(deleted_user)
        session.commit()
        flash("Bruker slettet :/")
        return redirect(url_for("usersroute.home"))
