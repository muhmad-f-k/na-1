from flask import Blueprint, render_template

dinner = Blueprint('dinner', __name__)


@dinner.route('/dinner')
def index():
    return render_template('dinner.html')
