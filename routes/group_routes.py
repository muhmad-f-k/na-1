from base64 import b64encode

from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import session, User, Comment, Edited_comment, Group, User_group_role, Role, Dinner
from flask_login import login_user, login_required, current_user, logout_user

grouproute = Blueprint('grouproute', __name__)

route_option = 0


@grouproute.route('/group/<group_id>')
@login_required
def show_group(group_id):
    admin_role = session.query(Role).filter(Role.name == "admin").first()
    dinners = session.query(Dinner).filter(Dinner.group_id == group_id).all()
    user_in_group = session.query(Group).join(
        User_group_role).filter(User_group_role.user_id == current_user.id, User_group_role.group_id == group_id).first()

    def decode_image2(image):
        if image is not None:
            picture = b64encode(image).decode("utf-8")
        else:
            picture = ""
        return picture

    if user_in_group is not None:
        current_user_role = session.query(User_group_role).filter(
            User_group_role.user_id == current_user.id,
            User_group_role.group_id == group_id).first()
        group = session.query(Group).select_from(User).join(User_group_role).join(
            Group).filter(Group.id == group_id).first()
        members = session.query(User_group_role).filter(User_group_role.group == group).all()
        for member in members:
            print(member.user_id)

        def decode_image(image):
            picture = b64encode(image).decode("utf-8")
            return picture

        return render_template("groups/group.html", group=group, current_user_role=current_user_role, members=members, decode_image=decode_image, dinners=dinners, admin_role=admin_role, decode_image2=decode_image2)

    if user_in_group is None:
        return render_template('errors/404.html'), 404


@grouproute.route('/group/<group_id>', methods=['POST'])
@login_required
def show_group_post(group_id):
    global route_option
    if request.form.get("action_add_member") == "legg til":
        add_member(group_id)
    if request.form.get("action_change_role") == "Lagre":
        change_role(group_id)
    if request.form.get("action_change_group_title") == "Endre":
        update_group(group_id)
    if request.form.get("action_remove_member") == "fjern_medlem":
        remove_member(group_id)
        if route_option == 1:
            return redirect(url_for('usersroute.home'))
    return redirect(url_for('grouproute.show_group', group_id=group_id))


def add_member(group_id):
    email = request.form.get('member_email')
    user_exists = session.query(User).filter(User.email == email).first()

    if user_exists is None:
        flash("medlemmet finnes ikke - Sjekk om riktig email", "warning")
        return redirect(url_for("grouproute.show_group", group_id=group_id))

    elif user_exists is not None:
        user_in_group = session.query(User_group_role).filter(
            User_group_role.user_id == user_exists.id, User_group_role.group_id == group_id).first()
        if user_in_group is None:
            role = session.query(Role).filter(Role.name == "gjest").first()
            assoc = User_group_role(user_id=user_exists.id, group_id=group_id, role_id=role.id)
            session.add(assoc)
            session.commit()
            session.close()
            flash("Nytt medlem i gruppen!", "success")
            return redirect(url_for("grouproute.show_group", group_id=group_id))
        elif user_in_group is not None:
            flash("medlemmet finnes allerede i gruppen", "info")
            return redirect(url_for("grouproute.show_group", group_id=group_id))


def change_role(group_id):
    member_id = request.form.get("member_id")
    new_role_id = request.form.get('rolle', type=int)
    member_count = session.query(User_group_role).filter(User_group_role.group_id == group_id).count()
    member = session.query(User_group_role).filter(
        User_group_role.user_id == member_id, User_group_role.group_id == group_id).first()
    admin_role = session.query(Role).filter(Role.name == "admin").first()
    moderator_role = session.query(Role).filter(Role.name == "moderator").first()
    admin = session.query(User_group_role).filter(
        User_group_role.role == admin_role, User_group_role.group_id == group_id).first()

    if member_count == 1 and new_role_id != admin_role.id:
        flash("Det må være en admin i gruppen, sorry not sorry", "warning")
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif admin.user == member.user and new_role_id != admin_role.id:
        flash("Det må være en admin i gruppen, velg en i gruppen du vil at skal være admin", "warning")
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif member.role_id == new_role_id:
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif new_role_id == admin_role.id and member.role != admin_role.id:
        admin.role = moderator_role
        session.commit()

    user_group = session.query(User_group_role).filter(
        User_group_role.user_id ==
        member_id, User_group_role.group_id == group_id).first()
    user_group.role_id = new_role_id
    session.commit()
    return redirect(url_for("grouproute.show_group", group_id=group_id))


def update_group(group_id):
    group = session.query(Group).filter(Group.id == group_id).first()
    group_name = request.form.get("group_name")
    already_existing_group_name = session.query(Group.name).filter(
        Group.name == group_name).first()

    if already_existing_group_name is not None:
        flash("Dette gruppenavnet er allerede tatt")
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif already_existing_group_name is None:
        group.name = group_name
        session.commit()
        flash("Gruppenavn endret!")
        return redirect(url_for('grouproute.show_group', group_id=group_id))


def remove_member(group_id):
    global route_option
    route_option = 0
    member_count = session.query(User_group_role).filter(User_group_role.group_id == group_id).count()
    admin_role = session.query(Role).filter(Role.name == "admin").first()
    moderator_role = session.query(Role).filter(Role.name == "moderator").first()
    cook_role = session.query(Role).filter(Role.name == "kokk").first()
    guest_role = session.query(Role).filter(Role.name == "gjest").first()
    admin = session.query(User_group_role).filter(
        User_group_role.role == admin_role, User_group_role.group_id == group_id).first()
    member_id = request.form.get("member_id")
    member = session.query(User_group_role).filter(
        User_group_role.group_id == group_id, User_group_role.user_id == member_id).first()

    if member_count == 1:
        flash("Det må alltid være en person i gruppen")
        route_option = 0

    elif member.user == admin.user:
        new_admin = session.query(User_group_role).filter(
            User_group_role.role == moderator_role, User_group_role.group_id == group_id).first()
        if new_admin is None:
            new_admin = session.query(User_group_role).filter(
                User_group_role.role == cook_role, User_group_role.group_id == group_id).first()
            if new_admin is None:
                new_admin = session.query(User_group_role).filter(
                    User_group_role.role == guest_role, User_group_role.group_id == group_id).first()
        new_admin.role = admin_role
        session.delete(member)
        session.commit()
        route_option = 1

    if route_option == 0 and member_count > 1:
        session.delete(member)
        session.commit()

# def delete_group(group_id):
#     group_to_delete = session.query(Group).filter(Group.id == group_id).first()
#     user_group_role_to_delete = session.query(User_group_role).filter(
#         User_group_role.group_id == group_id).all()
#     for i in user_group_role_to_delete:
#         session.delete(i)
#         session.commit()
#     session.delete(group_to_delete)
#     session.commit()
