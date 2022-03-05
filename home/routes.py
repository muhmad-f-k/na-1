from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home = Blueprint('simple_page', __name__, template_folder='templates')

home = Blueprint('home', __name__)


@home.route('/home')
def index():
    return render_template('index.html')
