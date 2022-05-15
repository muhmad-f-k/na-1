from sqlalchemy import desc

from db.modul import *

def get_dinner_object_with_dinner_id(dinner_id):
    return session.query(Dinner).filter(Dinner.id == dinner_id).first()

def get_highest_recipe_version_with_dinner_id(dinner_id):
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version

def get_highest_recipe_id_with_dinner_id(dinner_id):
    get_highest_recipe_version = session.query(Recipe.id).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version

def get_highest_recipe_versions_with_dinner_id(dinner_id):
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).all()
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
    add_object = Recipe(approach=approach,
           version=highest_recipe_version.version + 1,
            portions=highest_recipe_version.portions,
           dinner_id=dinner_id
           )
    session.add(add_object)
    session.commit()


def add_amount_to_table(amount):
    add_amount = Amount(amount=amount)
    session.add(add_amount)
    session.commit()

def add_ingredient_to_table(ingredient):
    add_ingredient = Ingredient(name=ingredient)
    session.add(add_ingredient)
    session.commit()

def copy_recipe_ingredient_helper(new_version, original_ingredients, original_amounts, original_measurements):
    for i in range(0, len(original_ingredients)):
        helper_object = Recipe_ingredient_helper(
            measurement_id=original_measurements[i].id,
            amount_id=original_amounts[i].id,
            ingredient_id=original_ingredients[i].id,
            recipe_id=new_version.id)
        session.add(helper_object)
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

def check_ingredient_in_table_and_get_object(ingredient):
    check_ingredient = session.query(Ingredient).filter(
        Ingredient.name == ingredient).first()
    if check_ingredient:
        return check_ingredient
    else:
        add_ingredient_to_table(ingredient)
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

def get_ingredient_ids_with_highest_recipe_version(recipe_id):
    return session.query(Ingredient.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def get_amount_ids_with_highest_recipe_version(recipe_id):
    return session.query(Amount.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def get_measurement_ids_with_highest_recipe_version(recipe_id):
    return session.query(Measurement.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def get_ingredient_with_name(ingredient):
    return session.query(Ingredient).filter(Ingredient.name == ingredient).first()


def get_amount_with_name(amount):
    return session.query(Amount).filter(Amount.amount == amount).first()

def get_measurement_with_measurement(measurement):
    return

def sum_up_amounts_and_get_object(prev_amount, new_amount):
    sum_amount = prev_amount + new_amount
    amount_obj = check_amount_in_table_and_get_object(sum_amount)
    return amount_obj


# user queries
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


# group queries
def members_in_group_count(group_id):
    return


def get_groups_with_user_id(id):
    return session.query(Group).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_group_with_group_name(name):
    return session.query(Group).filter(Group.name == name).first()


def get_group_join_with_user(group_id):
    return session.query(Group).select_from(User).join(User_group_role).join(
        Group).filter(Group.id == group_id).first()


def get_roles_with_user_id(id):
    return session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_user_group_role(user_id, group_id):
    return session.query(User_group_role).filter(
        User_group_role.user_id == user_id,
        User_group_role.group_id == group_id).first()


def get_members_in_group(group):
    return session.query(User_group_role).filter(User_group_role.group == group).all()


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


# shopping list queries
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

def get_dinner_by_dinner_id(dinner_id):
    return session.query(Dinner).filter(Dinner.id == dinner_id).first()
