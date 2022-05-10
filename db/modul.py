import os
import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DATE, LargeBinary, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_str = 'sqlite:///' + \
                 os.path.join(BASE_DIR, 'finaldata.db?check_same_thread=False')
engine = create_engine(connection_str)
base = declarative_base()


class User_group_role(base):
    __tablename__ = "user_group_role"

    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey(
        "group.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey(
        "role.id", ondelete="CASCADE"), nullable=False)
    UniqueConstraint('user_id', 'group_id', name='user_group')

    __table_args__ = (UniqueConstraint(user_id, group_id),)

    user = relationship("User", back_populates="user_group_role")
    group = relationship("Group", back_populates="user_group_role")
    role = relationship("Role", back_populates="user_group_role")


class User(base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    image = Column(LargeBinary(length=(2 ** 32) - 1))
    user_group_role = relationship(
        "User_group_role", back_populates="user", cascade="all, delete")
    dinner = relationship("Dinner")
    user = relationship("Comment")

    @property
    def password(self):
        raise AttributeError('password is unreadable by humans ')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.first_name} - {self.last_name} - {self.email} - {self.id}"


class Role(base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    user_group_role = relationship(
        "User_group_role", back_populates="role", cascade="all, delete")

    def __repr__(self):
        return f"{self.name} - {self.id}"


class Group(base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    user_group_role = relationship(
        "User_group_role", back_populates="group", cascade="all, delete")
    shopping_lists = relationship("Shopping_list")
    dinner = relationship("Dinner")
    meal = relationship("Meal")

    def __repr__(self):
        return f"{self.name} - {self.id}"


class Recipe_ingredient_helper(base):
    __tablename__ = "recipe_ingredient_helper"

    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    measurement_id = Column(Integer, ForeignKey(
        "measurement.id", ondelete="CASCADE"), nullable=False)
    amount_id = Column(Integer, ForeignKey(
        "amount.id", ondelete="CASCADE"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(
        "ingredient.id", ondelete="CASCADE"), nullable=False)
    recipe_id = Column(Integer, ForeignKey(
        "recipe.id", ondelete="CASCADE"), nullable=False)
    UniqueConstraint('ingredient_id', 'recipe_id', name='ingredient_recipe')

    __table_args__ = (UniqueConstraint(
        measurement_id, ingredient_id, recipe_id, amount_id),)

    measurement = relationship(
        "Measurement", back_populates="recipe_ingredient_helper")
    ingredient = relationship(
        "Ingredient", back_populates="recipe_ingredient_helper")
    recipe = relationship("Recipe", back_populates="recipe_ingredient_helper")
    amount = relationship("Amount", back_populates="recipe_ingredient_helper")


class Shopping_list(base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    date = Column(DATE(), default=datetime.date.today(), nullable=False)
    price = Column(String(10), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.date} - {self.price} - {self.week_number} - {self.year}"


class Measurement(base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    name = Column(String(10), nullable=False, unique=True)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="measurement", cascade="all, delete")

    def __repr__(self):
        return f"{self.id} - {self.name}"


class Recipe(base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    approach = Column(String(20000), nullable=False)
    version = Column(Integer, nullable=False)
    portions = Column(Integer, nullable=True)
    UniqueConstraint('id', 'version', name='id_version')
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="recipe", cascade="all, delete")
    dinner_id = Column(Integer, ForeignKey(
        "dinner.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.approach} - {self.portions}"


class Ingredient(base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    name = Column(String(45), nullable=False, unique=True)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="ingredient", cascade="all, delete")

    def __repr__(self):
        return f"{self.id} - {self.name}"


class Dinner(base):
    __tablename__ = "dinner"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    image = Column(LargeBinary(length=(2 ** 32) - 1))
    recipe = relationship("Recipe", cascade="all, delete")
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = relationship("Comment")
    meal = relationship("Meal")

    def __repr__(self):
        return f"{self.id} - {self.title}"


class Meal(base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    date = Column(DATE(), default=datetime.date.today(), nullable=False)
    portions = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    dinner_id = Column(Integer, ForeignKey("dinner.id"), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.date} - {self.portions}"


class Comment(base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    text = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dinner_id = Column(Integer, ForeignKey("dinner.id"), nullable=False)
    comment = relationship("Edited_comment")

    def __repr__(self):
        return f"{self.id} - {self.text}"


class Edited_comment(base):
    __tablename__ = "edited_comment"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    text = Column(String(100), nullable=False)
    comment_id = Column(Integer, ForeignKey("comment.id"), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.text}"


class Deleted_comment(base):
    __tablename__ = "deleted_comment"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    text = Column(String(100), nullable=False)
    dinner_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.text} - {self.dinner_id} - {self.user_id}"


class Amount(base):
    __tablename__ = "amount"
    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    amount = Column(Integer, nullable=False)
    recipe_ingredient_helper = relationship(
        "Recipe_ingredient_helper", back_populates="amount")

    def __repr__(self):
        return f"{self.id} - {self.amount}"


base.metadata.create_all(engine)
session = sessionmaker()(bind=engine)
