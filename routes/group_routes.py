from base64 import b64encode
import queries
from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import session, User, Comment, Edited_comment, Group, User_group_role, Role, Dinner
from flask_login import login_user, login_required, current_user, logout_user

grouproute = Blueprint('grouproute', __name__)

route_option = 0


@grouproute.route('/group/<group_id>')
@login_required
def show_group(group_id):
    admin_role = queries.get_role_by_name("admin")
    moderator_role = queries.get_role_by_name("moderator")
    cook_role = queries.get_role_by_name("kokk")
    guest_role = queries.get_role_by_name("gjest")
    dinners = queries.get_dinners_by_group(group_id)
    user_in_group = queries.get_user_in_group(group_id, current_user.id)

    def decode_image2(image):
        if image is not None:
            picture = b64encode(image).decode("utf-8")
        else:
            picture = ""
        return picture

    if user_in_group is not None:
        current_user_role = queries.get_user_group_role(current_user.id, group_id)
        group = queries.get_group_join_with_user(group_id)
        members = queries.get_members_in_group(group)

        def decode_image(image):
            picture = b64encode(image).decode("utf-8")
            return picture

        return render_template("groups/group.html", group=group, current_user_role=current_user_role, members=members, decode_image=decode_image, dinners=dinners, admin_role=admin_role, moderator_role=moderator_role, cook_role=cook_role, guest_role=guest_role, decode_image2=decode_image2)

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
    user_exists = queries.get_user_by_email(email)

    if user_exists is None:
        flash("medlemmet finnes ikke - Sjekk om riktig email", "warning")
        return redirect(url_for("grouproute.show_group", group_id=group_id))

    elif user_exists is not None:
        user_in_group = queries.get_user_group_role(user_exists.id, group_id)
        if user_in_group is None:
            role = queries.get_role_by_name("gjest")
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
    new_role_id = int(request.form.get('rolle'))
    member_count = queries.members_in_group_count(group_id)
    member = queries.get_user_group_role(member_id, group_id)
    admin_role = queries.get_role_by_name("admin")
    moderator_role = queries.get_role_by_name("moderator")
    admin = queries.get_admin_in_group(admin_role, group_id)

    if member_count == 1 and new_role_id != admin_role.id:
        flash("Det må være en admin i gruppen, sorry not sorry", "warning")
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif admin.user == member.user and new_role_id != admin_role.id:
        flash("Det må være en admin i gruppen, velg en i gruppen du vil at skal være admin", "warning")
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif member.role_id == new_role_id:
        return redirect(url_for('grouproute.show_group', group_id=group_id))

    elif new_role_id == admin_role.id and member.role != admin_role:
        admin.role = moderator_role
        session.commit()

    user_group = queries.get_user_group_role(member_id, group_id)
    user_group.role_id = new_role_id
    session.commit()
    return redirect(url_for("grouproute.show_group", group_id=group_id))


def update_group(group_id):
    group = queries.get_group_with_group_id(group_id)
    group_name = request.form.get("group_name")
    already_existing_group_name = queries.get_group_with_group_name(group_name)

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
    member_count = queries.members_in_group_count(group_id)
    admin_role = queries.get_role_by_name("admin")
    moderator_role = queries.get_role_by_name("moderator")
    cook_role = queries.get_role_by_name("kokk")
    guest_role = queries.get_role_by_name("gjest")
    admin = queries.get_admin_in_group(admin_role, group_id)
    member_id = request.form.get("member_id")
    member = queries.get_user_group_role(member_id, group_id)

    if member_count == 1:
        flash("Det må alltid være en person i gruppen")
        route_option = 0

    elif member.user == admin.user:
        new_admin = queries.get_moderator_in_group(moderator_role, group_id)
        if new_admin is None:
            new_admin = queries.get_cook_in_group(cook_role, group_id)
            if new_admin is None:
                new_admin = queries.get_guest_in_group(guest_role, group_id)
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
