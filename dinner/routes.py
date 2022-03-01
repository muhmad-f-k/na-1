from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import RegistrationForm

dinner = Blueprint('dinner', __name__)


@dinner.route('/dinner', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    return render_template('dinner.html', form=form)
