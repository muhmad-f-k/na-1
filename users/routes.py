from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from users import *
users = Blueprint('users', __name__, template_folder="templates")


@users.route('/user')
def index():
    form = RegistrationForm()
    return render_template('loginTemplates/user.html', form=form)


@users.route('/register')
def register():
    form = RegistrationForm()
    return render_template('loginTemplates/register.html', form=form)
