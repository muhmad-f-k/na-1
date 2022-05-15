from db.modul import *
from sqlalchemy import func, cast, Float, desc


def save_user_details(email, first_name, last_name, set_password):
    new_user = User(email=email, first_name=first_name,
                    last_name=last_name, set_password=set_password)
    session.add(new_user)
    session.commit()
    session.close()
    return new_user


def get_user_by_email(email):
    return session.query(User).filter(
        User.email == email).first()


def detete_user_by_id(id):
    delete_user = session.query(User).filter_by(id=id).first()
    session.delete(delete_user)
    session.commit()
    return delete_user


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


def get_all_group_role_for_user(user_id):
    return session.query(User_group_role).filter(
        User_group_role.user_id == user_id).all()


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
    return session.query(Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).order_by(
        desc(Recipe.version)).first()


def get_highest_recipe_version_with_dinner_id(dinner_id):
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version


def add_new_recipe(approach, dinner_id, portions):
    recipe_object = Recipe(
        approach=approach, version=1, portions=portions, dinner_id=dinner_id)
    session.add(recipe_object)
    session.commit()
    return recipe_object


def get_all_measurements():
    return session.query(Measurement).all()


def add_new_version_to_recipe(approach, dinner_id):
    highest_recipe_version = get_highest_recipe_version_with_dinner_id(dinner_id)
    Recipe(approach=approach,
           version=highest_recipe_version.version + 1,
           dinner_id=dinner_id,
           portions=highest_recipe_version.portions)
    session.add(add_new_version_to_recipe)
    session.commit()
    return


def add_amount_to_table(amount):
    add_amount = Amount(amount=amount)
    session.add(add_amount)
    session.commit()


def check_amount_in_table_and_get_object(amount):
    check_amount = session.query(Amount).filter(
        Amount.amount == amount).first()
    if check_amount:
        return check_amount
    else:
        add_amount_to_table(amount)
        return session.query(Amount).filter(
            Amount.amount == amount).first()


def get_ingredient_names_with_recipe_id(recipe_id):
    return session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_amount_amounts_with_recipe_id(recipe_id):
    return session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_measurement_measurements_with_recipe_id(recipe_id):
    return session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_ingredients_with_highest_recipe_version(highest_recipe_version):
    return session.query(Ingredient.id).join(
        Recipe_ingredient_helper).filter(
        Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_amounts_with_highest_recipe_version(highest_recipe_version):
    return session.query(Amount.id).join(Recipe_ingredient_helper).filter(
        Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_measurements_with_highest_recipe_version(highest_recipe_version):
    return session.query(Measurement.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == highest_recipe_version.id).all()


def get_ingredient_with_name(ingredient):
    return session.query(Ingredient).filter(Ingredient.name == ingredient).first()


def get_amount_with_name(ingredient):
    return session.query(Ingredient).filter(Ingredient.name == ingredient).first()


def sum_up_amounts_and_get_object(prev_amount, new_amount):
    sum_amount = prev_amount + new_amount
    amount_obj = check_amount_in_table_and_get_object(sum_amount)
    return amount_obj
