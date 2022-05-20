from db.modul import *
from sqlalchemy import func, cast, Float, desc


def save_user_details(email, first_name, last_name, set_password):
    """This method creates a new user"""
    new_user = User(email=email, first_name=first_name,
                    last_name=last_name, set_password=set_password)
    session.add(new_user)
    session.commit()
    session.close()
    return new_user


def get_user_by_email(email):
    """This method returns a user with the correct email"""
    return session.query(User).filter(
        User.email == email).first()


def detete_user_by_id(id):
    """This method deletes a user"""
    delete_user = session.query(User).filter_by(id=id).first()
    session.delete(delete_user)
    session.commit()
    return delete_user


def get_user_by_id(id):
    """This method returns a user with the correct id"""
    return session.query(User).filter(User.id == id).first()


def get_user_in_group(group_id, user_id):
    """This method returns a user from the database with the correct user and group id"""
    return session.query(Group).join(
        User_group_role).filter(User_group_role.user_id == user_id, User_group_role.group_id == group_id).first()


def members_in_group_count(group_id):
    """This method returns the number og members in a group"""
    return session.query(User_group_role).filter(User_group_role.group_id == group_id).count()


def get_groups_with_user_id(id):
    """This method returns all groups that a user is part of, and the user's role within them"""
    return session.query(Group).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_group_with_group_name(name):
    """This method returns a group with the correct name"""
    return session.query(Group).filter(Group.name == name).first()


def get_group_join_with_user(group_id):
    """This method returns group, group role and user with the correct group id"""
    return session.query(Group).select_from(User).join(User_group_role).join(
        Group).filter(Group.id == group_id).first()


def get_group_with_group_id(group_id):
    """This method returns a group with the correct id"""
    return session.query(Group).filter(Group.id == group_id).first()


def get_roles_with_user_id(id):
    """This method returns the names of all group roles that a user has"""
    return session.query(Role.name).join(
        User_group_role).join(User).filter(User.id == id).all()


def get_user_group_role(user_id, group_id):
    """This method returns the group role of the user from a specific group"""
    return session.query(User_group_role).filter(
        User_group_role.user_id == user_id,
        User_group_role.group_id == group_id).first()


def get_members_in_group(group):
    """This method returns all members of a group"""
    return session.query(User_group_role).filter(User_group_role.group == group).all()


def get_admin_in_group(admin_role, group_id):
    """This method returns the user that has the admin role in a specific group"""
    return session.query(User_group_role).filter(
        User_group_role.role == admin_role, User_group_role.group_id == group_id).first()


def get_moderator_in_group(moderator_role, group_id):
    """This method returns the user that has the moderator role in a specific group"""
    return session.query(User_group_role).filter(
        User_group_role.role == moderator_role, User_group_role.group_id == group_id).first()


def get_cook_in_group(cook_role, group_id):
    """This method returns the user that has the cook role in a specific group"""
    return session.query(User_group_role).filter(
        User_group_role.role == cook_role, User_group_role.group_id == group_id).first()


def get_guest_in_group(guest_role, group_id):
    """This method returns the user that has the guest role in a specific group"""
    return session.query(User_group_role).filter(
        User_group_role.role == guest_role, User_group_role.group_id == group_id).first()


def save_group_name(name):
    """This method creates and returns a group"""
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    return group


def get_role_by_name(name):
    """This method returns a role object with the correct name"""
    return session.query(Role).filter(Role.name == name).first()


def save_role_group(user_id, group_id, role_id):
    """This method creates a user-role-group relationship and returns it"""
    add_role_group = User_group_role(user_id=user_id,
                                     group_id=group_id, role_id=role_id)
    session.add(add_role_group)
    session.commit()
    session.close()
    return add_role_group


def get_shopping_list_data(group_id, monday, sunday):
    """This method returns shopping list data between a monday and sunday"""
    return session.query(Ingredient.name,
                         func.round(func.sum(cast(Amount.amount, Float) / Recipe.portions * Meal.portions), 1),
                         Measurement.name). \
        select_from(Meal).join(Dinner).join(Recipe).join(Recipe_ingredient_helper).join(Ingredient).join(Measurement). \
        join(Amount).filter(Dinner.id == Meal.dinner_id, Meal.group_id == group_id, Meal.date.between(monday, sunday)). \
        group_by(Ingredient.name, Measurement.name).all()


def get_shopping_list_object(group_id, year, week_number):
    """This method returns a shopping list object between a monday and sunday"""
    return session.query(Shopping_list).filter(
        Shopping_list.year == year, Shopping_list.week_number == week_number,
        Shopping_list.group_id == group_id).first()


def undo_shopping_list(group_id, year, week_number):
    """This method deletes a shopping list"""
    shopping_list = session.query(Shopping_list).filter(
        Shopping_list.year == year, Shopping_list.week_number == week_number,
        Shopping_list.group_id == group_id).first()
    session.delete(shopping_list)
    session.commit()
    session.close()


def get_dinners_by_group(group_id):
    """This method returns all dinner belonging to a specific group"""
    return session.query(Dinner).filter(Dinner.group_id == group_id).all()


def get_ingredient_by_name(name):
    """This method returns an ingredient with the correct name"""
    return session.query(Ingredient).filter(Ingredient.name == name).first()


def get_amount_by_amount(amount):
    """This method returns an amount with a specific amount"""
    return session.query(Amount).filter(Amount.amount == amount).first()


def get_measurement_by_name(name):
    """This method returns a measurement type with the correct name"""
    return session.query(Measurement).filter(Measurement.name == name).first()


def get_recipe_with_dinner_id(dinner_id):
    """This method returns recipe from a specific dinner"""
    return session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(desc(Recipe.version)).first()


def get_approach_by_approach(approach):
    """This method returns a recipe approach whith a specific approach"""
    return session.query(Recipe).filter(Recipe.approach == approach).first()


def check_recipe_ingredient_helper_by_recipe_id(recipe_id):
    """This method returns a recipe ingredient helper"""
    return session.query(Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).order_by(
        desc(Recipe.version)).first()


def delete_meal_with_id(meal_id):
    """This method deletes a meal with a specific id"""
    session.query(Meal).filter_by(id=meal_id).delete()
    session.commit()
    session.close()


def portion(meal_id, new_portion):
    """This method sets a new portion number for a meal"""
    meal = session.query(Meal).filter(Meal.id == meal_id).first()
    meal.portions = new_portion
    session.commit()
    session.close()


def get_meal_joined_with_dinner_with_group_id(group_id, i):
    """This method returns a meal and dinner from a specific group and date"""
    meal = session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(
        Meal.group_id == group_id).filter(Meal.date == i.date()).first()
    session.close()
    return meal


def get_meal_joined_with_dinner_without_group_id(i):
    """This method returns a meal and dinner from a date"""
    meal = session.query(Meal, Dinner).filter(Meal.dinner_id == Dinner.id).filter(Meal.date == i).first()
    session.close()
    return meal


def get_current_user_role_with_group_id(current_user, group_id):
    """This method returns the group role of the current user in a specific group"""
    return session.query(User_group_role).filter(User_group_role.user_id == current_user.id,
                                                 User_group_role.group_id == group_id).first()


def create_meal(meal):
    """This method creates a meal"""
    session.add(meal)
    session.commit()


def create_dinner(dinner):
    """This method creates a dinner"""
    session.add(dinner)
    session.commit()


def get_dinner_by_id(dinner_id):
    """This method returns a dinner with the correct id"""
    return session.query(Dinner).filter(Dinner.id == dinner_id).first()


def get_comments_by_dinner_id(dinner_id):
    """This method returns comments with the correct dinner id"""
    return session.query(Comment).filter(Comment.dinner_id == dinner_id).all()


def get_ingredients_by_recipe_id(recipe):

    """This method returns all ingredients with the correct recipe id"""
    return session.query(Ingredient.name).join(Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()



def get_amounts_by_recipe_id(recipe):
    """This method returns all amounts with the correct recipe id"""
    return session.query(Amount.amount).join(Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()


def get_measurements_by_recipe_id(recipe):
    """This method returns all measurement names with the correct recipe id"""
    return session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe.id).all()


def create_shopping_list(shopping_list):
    """This method creates a shopping list"""
    session.add(shopping_list)
    session.commit()


def create_comment(comment):
    """This method creates a comment"""
    session.add(comment)
    session.commit()


def get_comment_by_id(comment_id):
    """This method returns a comment with the correct id"""
    return session.query(Comment).filter(Comment.id == comment_id).first()


def create_edited_comment(copy_data_to_edit_comment):
    """This method creates an edited comment"""
    session.add(copy_data_to_edit_comment)


def get_edited_comments_by_comment_id(comment_id):
    """This method returns all edited comments with the correct comment id"""
    return session.query(Edited_comment).filter(Edited_comment.comment_id == comment_id).all()


def delete_comment_by_id(comment_id):
    """This method deletes a comment with the correct id"""
    delete_comment = session.query(Comment).filter(Comment.id == comment_id).first()
    session.delete(delete_comment)
    session.commit()


def add_new_recipe(approach, dinner_id, portions):
    """This method creates a new recipe"""
    recipe_object = Recipe(
        approach=approach, version=1, portions=portions, dinner_id=dinner_id)
    session.add(recipe_object)
    session.commit()
    return


def get_all_measurements():
    """This method returns all measurements"""
    return session.query(Measurement).all()


def get_ingredient_names_with_recipe_id(recipe_id):
    """This method returns all ingredient's names with the correct recipe id"""
    return session.query(Ingredient.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_amount_amounts_with_recipe_id(recipe_id):
    """This method returns all amount's amounts with the correct recipe id"""
    return session.query(Amount.amount).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_measurement_measurements_with_recipe_id(recipe_id):
    """This method returns all measurement's measurement with the correct recipe id"""
    return session.query(Measurement.name).join(
        Recipe_ingredient_helper).join(Recipe).filter(Recipe.id == recipe_id).all()


def get_highest_recipe_version_with_dinner_id(dinner_id):
    """This method returns the newest recipe with the correct dinner id"""
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version


def add_ingredient_to_table(ingredient):
    """This method creates a new ingredient"""
    add_ingredient = Ingredient(name=ingredient)
    session.add(add_ingredient)
    session.commit()


def check_ingredient_in_table_and_get_object(ingredient):
    """This method checks if an ingredient already exists, if true returns true,
     if false add it to the database and returns the ingredient's name"""
    check_ingredient = session.query(Ingredient).filter(
        Ingredient.name == ingredient).first()
    if check_ingredient:
        return check_ingredient
    else:
        add_ingredient_to_table(ingredient)
        return session.query(Amount).filter(
            Ingredient.name == ingredient).first()


def sum_up_amounts_and_get_object(prev_amount, new_amount):
    """This method returns the sum of the two provided amounts"""
    sum_amount = prev_amount + new_amount
    amount_obj = check_amount_in_table_and_get_object(sum_amount)
    return amount_obj


def check_amount_in_table_and_get_object(amount):
    """This method checks if an amount already exists, if true returns true,
         if false add it to the database and returns the amount's amount"""
    check_amount = session.query(Amount).filter(
        Amount.amount == amount).first()
    if check_amount:
        return check_amount
    else:
        add_amount_to_table(amount)
        return session.query(Amount).filter(
            Amount.amount == amount).first()


def add_amount_to_table(amount):
    """This method creates a new amount"""
    add_amount = Amount(amount=amount)
    session.add(add_amount)
    session.commit()


def add_new_version_to_recipe(approach, dinner_id):
    """this method creates a new recipe and makes it a version of an existing one"""
    highest_recipe_version = get_highest_recipe_version_with_dinner_id(dinner_id)
    add_object = Recipe(approach=approach,
                        version=highest_recipe_version.version + 1,
                        portions=highest_recipe_version.portions,
                        dinner_id=dinner_id
                        )
    session.add(add_object)
    session.commit()


def get_ingredient_ids_with_highest_recipe_version(recipe_id):
    """this method returns the ingredients of the newest recipe of a dinner"""
    return session.query(Ingredient.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def get_amount_ids_with_highest_recipe_version(recipe_id):
    """this method returns the amount id's of a dinner's newest recipe"""
    return session.query(Amount.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def get_measurement_ids_with_highest_recipe_version(recipe_id):
    """this method returns the measurement id's of a dinner's newest recipe"""
    return session.query(Measurement.id).join(
        Recipe_ingredient_helper).filter(Recipe_ingredient_helper.recipe_id == recipe_id).all()


def copy_recipe_ingredient_helper(new_version, original_ingredients, original_amounts, original_measurements):
    """this method makes a cope of a recipe ingredient helper"""
    for i in range(0, len(original_ingredients)):
        helper_object = Recipe_ingredient_helper(
            measurement_id=original_measurements[i].id,
            amount_id=original_amounts[i].id,
            ingredient_id=original_ingredients[i].id,
            recipe_id=new_version.id)
        session.add(helper_object)
        session.commit()


def get_dinner_object_with_dinner_id(dinner_id):
    """this method returns a dinner with the correct id"""
    return session.query(Dinner).filter(Dinner.id == dinner_id).first()


def get_highest_recipe_versions_with_dinner_id(dinner_id):
    """this method returns all recipes of a dinner in descending version number order"""
    get_highest_recipe_version = session.query(Recipe).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).all()
    return get_highest_recipe_version


#############
def get_all_group_role_for_user(user_id):
    """this method returns all roles a user has"""
    return session.query(User_group_role).filter(
        User_group_role.user_id == user_id).all()


def get_highest_recipe_id_with_dinner_id(dinner_id):
    """this method returns the recipe id of the newest recipe of a dinner"""
    get_highest_recipe_version = session.query(Recipe.id).filter(Recipe.dinner_id == dinner_id).order_by(
        desc(Recipe.version)).first()
    return get_highest_recipe_version


def get_ingredient_with_name(ingredient):
    """this method returns an ingredient with the correct name"""
    return session.query(Ingredient).filter(Ingredient.name == ingredient).first()


def get_amount_with_name(amount):
    """this method returns an amount with the correct name"""
    return session.query(Amount).filter(Amount.amount == amount).first()
