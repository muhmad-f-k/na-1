from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from users.forms import RegistrationForm

users = Blueprint('users', __name__)


@users.route('/user')
def index():
    form = RegistrationForm()
    return render_template('user.html', form=form)


@users.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)