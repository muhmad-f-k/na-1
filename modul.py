import os
from sqlalchemy import BLOB, Column, String, Integer, ForeignKey, create_engine, Table, DATE, DECIMAL, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_str = 'sqlite:///'+os.path.join(BASE_DIR, 'finaldata.db')
engine = create_engine(connection_str)
base = declarative_base()


class User_group_role(base):
    __tablename__ = "user_group_role"

    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    __table_args__ = (UniqueConstraint(user_id, group_id, role_id),)

    user = relationship("User", back_populates="user_group_role")
    group = relationship("Group", back_populates="user_group_role")
    role = relationship("Role", back_populates="user_group_role")


class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    email = Column(String(50))
    password = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_group_role = relationship("User_group_role", back_populates="user")
    dinner = relationship("Dinner")
    user = relationship("Comment")


class Role(base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    name = Column(String(255))
    user_group_role = relationship("User_group_role", back_populates="role")


class Group(base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    name = Column(String(255))
    user_group_role = relationship("User_group_role", back_populates="group")
    shopping_lists = relationship("Shopping_list")
    dinner = relationship("Dinner")


class Recipe_ingredient_helper(base):
    __tablename__ = "recipe_ingredient_helper"

    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    recipe_ingredient_id = Column(Integer, ForeignKey(
        "recipe_ingredient.id"), nullable=False)
    measurement_id = Column(Integer, ForeignKey(
        "measurement.id"), nullable=False)
    shopping_list_id = Column(Integer, ForeignKey(
        "shopping_list.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(
        "ingredient.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)

    __table_args__ = (UniqueConstraint(recipe_ingredient_id,
                      measurement_id, ingredient_id, recipe_id, shopping_list_id),)

    recipe_ingredient = relationship(
        "Recipe_ingredient", back_populates="recipe_ingredient_helper")
    measurement = relationship(
        "Measurement", back_populates="recipe_ingredient_helper")
    shopping_list = relationship(
        "Shopping_list", back_populates="recipe_ingredient_helper")
    ingredient = relationship(
        "Ingredient", back_populates="recipe_ingredient_helper")
    recipe = relationship("Recipe", back_populates="recipe_ingredient_helper")


class Recipe_ingredient(base):
    __tablename__ = "recipe_ingredient"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    amount = Column(Integer, nullable=False)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="recipe_ingredient")


class Shopping_list(base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    date = Column(DATE, nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="shopping_list")


class Measurement(base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    amount = Column(String(10), nullable=False)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="measurement")


class Recipe(base):  # many
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    approach = Column(String(20000), nullable=False)
    version = Column(Integer, nullable=False)# sjekk ut longtext
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="recipe")
    dinner_id = Column(Integer, ForeignKey("dinner.id"))


class Ingredient(base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    name = Column(String(45), nullable=False)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="ingredient")


class Dinner(base):
    __tablename__ = "dinner"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    image = Column(LargeBinary(length=(2**32)-1))
    recipe = relationship("Recipe")
    group_id = Column(Integer, ForeignKey("group.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = relationship("Comment")
    meal = relationship("Meal")


class Meal(base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    date = Column(DATE, nullable=False)
    dinner_id = Column(Integer, ForeignKey("dinner.id"))


class Comment(base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    text = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    dinner_id = Column(Integer, ForeignKey("dinner.id"))
    comment = relationship("Edited_comment")


class Edited_comment(base):
    __tablename__ = "edited_comment"
    id = Column(Integer, primary_key=True, index=True,
                nullable=False, autoincrement=True)
    text = Column(String(100), nullable=False)
    comment_id = Column(Integer, ForeignKey("comment.id"))


base.metadata.create_all(engine)
session = sessionmaker()(bind=engine)
