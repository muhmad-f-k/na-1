from db.modul import *
from sqlalchemy import func, cast, Float, desc


def get_user_by_email(email):
    return session.query(User).filter(
        User.email == email).first()


def detete_user_by_id(id):
    return session.query(User).filter_by(id=id).delete()


def get_user_by_id(id):
    return session.query(User).filter(User.id == id).first()


def get_user_in_group(group_id, user_id):
    return session.query(Group).join(
        User_group_role).filter(User_group_role.user_id == user_id, User_group_role.group_id == group_id).first()


def members_in_group_count(group_id):
    return session.query(User_group_role).filter(User_group_role.group_id == group_id).count()


def get_groups_with_user_id(id):
    return session.query(Group).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_group_with_group_name(name):
    return session.query(Group).filter(Group.name == name).first()


def get_group_join_with_user(group_id):
    return session.query(Group).select_from(User).join(User_group_role).join(
            Group).filter(Group.id == group_id).first()


def get_group_with_group_id(group_id):
    return session.query(Group).filter(Group.id == group_id).first()


def get_roles_with_user_id(id):
    return session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_user_group_role(user_id, group_id):
    return session.query(User_group_role).filter(
        User_group_role.user_id == user_id,
        User_group_role.group_id == group_id).first()


def get_members_in_group(group):
    return session.query(User_group_role).filter(User_group_role.group == group).all()


def get_admin_in_group(admin_role, group_id):
    return session.query(User_group_role).filter(
        User_group_role.role == admin_role, User_group_role.group_id == group_id).first()


def get_moderator_in_group(moderator_role, group_id):
    return session.query(User_group_role).filter(
            User_group_role.role == moderator_role, User_group_role.group_id == group_id).first()


def get_cook_in_group(cook_role, group_id):
    return session.query(User_group_role).filter(
                User_group_role.role == cook_role, User_group_role.group_id == group_id).first()


def get_guest_in_group(guest_role, group_id):
    return session.query(User_group_role).filter(
                    User_group_role.role == guest_role, User_group_role.group_id == group_id).first()


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


def get_shopping_list_data(group_id, monday, sunday):
    return session.query(Ingredient.name,
                         func.round(func.sum(cast(Amount.amount, Float) / Recipe.portions * Meal.portions), 1),
                         Measurement.name). \
        select_from(Meal).join(Dinner).join(Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement). \
        join(Amount).filter(Dinner.id == Meal.dinner_id, Meal.group_id == group_id, Meal.date.between(monday, sunday)). \
        group_by(Ingredient.name, Measurement.name).all()


def get_shopping_list_object(group_id, year, week_number):
    return session.query(Shopping_list).filter(
        Shopping_list.year == year, Shopping_list.week_number == week_number,
        Shopping_list.group_id == group_id).first()


def undo_shopping_list(group_id, year, week_number):
    shopping_list = session.query(Shopping_list).filter(
        Shopping_list.year == year, Shopping_list.week_number == week_number,
        Shopping_list.group_id == group_id).first()
    session.delete(shopping_list)
    session.commit()
    session.close()


def get_dinners_by_group(group_id):
    return session.query(Dinner).filter(Dinner.group_id == group_id).all()


def get_ingredient_by_name(name):
    return session.query(Ingredient).filter(Ingredient.name == name).first()


def get_amount_by_amount(amount):
    return session.query(Amount).filter(Amount.amount == amount).first()


def get_measurement_by_name(name):
    return session.query(Measurement).filter(Measurement.name == name).first()


def get_recipe_with_dinner_id(dinner_id):
    return session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(desc(Recipe.version)).first()


def get_approach_by_approach(approach):
    return session.query(Recipe).filter(Recipe.approach == approach).first()


def check_recipe_ingredient_helper_by_recipe_id(recipe_id):
    return session.query(Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).order_by(desc(Recipe.version)).first()
