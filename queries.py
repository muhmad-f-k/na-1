""" from db.modul import *


def get_user_by_email(email):
    return session.query(User).filter(
        User.email == email).first()


def detete_user_by_id(id):
    return session.query(User).filter_by(id=id).delete()


def get_user_by_id(id):
    return session.query(User).filter(User.id == id).first()


def get_groups_with_user_id(id):
    return session.query(Group).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_group_with_group_name(name):
    return session.query(Group).filter(Group.name == name).first()


def get_roles_with_user_id(id):
    return session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == id).all()


def save_group_name(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    return group


def get_role_by_name(name):
    return session.query(Role).filter(Role.name == name).first()


def save_role_group(user_id, group_id, role_id):
    add_role_group = User_group_role(user_id=user_id,
                                     group_id=group_id, role_id=role_id)
    session.add(add_role_group)
    session.commit()
    session.close()
    return add_role_group
 """