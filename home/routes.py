from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/', defaults={'page': 'index'})
def index():
    return render_template('index.html')