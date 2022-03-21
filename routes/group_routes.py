from flask import Blueprint, redirect, render_template, request, url_for, flash
from db.modul import session, User, Comment, Edited_comment, Group, User_group_role, Role
from flask_login import login_user, login_required, current_user, logout_user

grouproute = Blueprint('grouproute', __name__)


@grouproute.route('/groups')
@login_required
def groups():
    groups = session.query(Group).join(
        User_group_role).join(User).filter(User.id == current_user.id).all()
    session.close()

    return render_template('groups.html', groups=groups)


@grouproute.route('/group/<group_id>')
@login_required
def show_group(group_id):
    group = session.query(Group).filter(Group.id == group_id).first()
    session.close()

    return render_template("group.html", group=group)


@grouproute.route('/create_group')
def create_group():
    return render_template("createGroup.html")


@grouproute.route('/create_group', methods=['POST'])
@login_required
def create_group_post():
    name = request.form.get("group_name")
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    role = session.query(Role).filter(Role.name == "admin").first()
    session.close()
    assoc = User_group_role(user=current_user, group=group, role=role)
    session.add(assoc)
    session.commit()
    session.close()

    return redirect(url_for("usersroute.profile"))


@grouproute.route('/group_members/<group_id>')
@login_required
def member_list(group_id):
    group = session.query(Group).filter(Group.id == group_id).first()
    members = session.query(User).join(
        User_group_role).join(Group).filter(Group.id == group_id).all()
    session.close()

    return render_template("groupMembers.html", members=members, group=group)


@grouproute.route("/group_members/<group_id>", methods=['POST'])
@login_required
def member_list_post(group_id):
    member_id = request.form.get("member_id")
    group = session.query(Group).filter(Group.id == group_id).first()
    new_role_id = request.form.get("member_role")

    current_user_role = session.query(User_group_role).filter(
        User_group_role.user_id == current_user.id,
        User_group_role.group_id == group_id).first()

    if current_user_role.role_id == 1:
        user_group = session.query(User_group_role).filter(
            User_group_role.user_id ==
            member_id, User_group_role.group_id == group_id).first()

        user_group.role_id = new_role_id
        session.commit()
    else:
        flash("Du har ikke rettighetene til å endre roller")
        return redirect(url_for("grouproute.member_list", group_id=group_id))

    return redirect(url_for("grouproute.member_list", group_id=group_id))


@grouproute.route('/update_group/<group_id>')
def update_group(group_id):
    group_to_update = session.query(Group).get(group_id)
    return render_template("update_group.html", group=group_to_update)


@grouproute.route('/update_group/<group_id>', methods=['POST'])
def update_group_post(group_id):
    group = session.query(Group).get(group_id)
    group.name = request.form.get("new_group_name")
    session.commit()

    return redirect(url_for("grouproute.groups", group_id=group_id))


@grouproute.route('/delete_group/<group_id>/')
def delete_group(group_id):
    group_to_delete = session.query(Group).get(group_id)
    print(group_to_delete.id)
    return render_template("delete_group.html")


@grouproute.route('/delete_group/<group_id>/', methods=['POST'])
def delete_group_post(group_id):
    group_to_delete = session.query(Group).get(group_id)
    user_group_role_to_delete = session.query(User_group_role).filter(
        User_group_role.group_id == group_id).first()
    session.delete(user_group_role_to_delete)
    print(group_to_delete.name)
    session.delete(group_to_delete)
    session.commit()

    return redirect(url_for("grouproute.groups", group_id=group_id))
