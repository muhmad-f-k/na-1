from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from dinner.forms import RegistrationForm

dinner = Blueprint('dinner', __name__)


@dinner.route('/dinner')
def index():
    form = RegistrationForm()
    return render_template('dinner.html', form=form)
