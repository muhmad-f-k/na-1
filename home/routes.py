from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from home import *
home = Blueprint('simple_page', __name__, template_folder="templates")


@home.route('/home')
def index():
    return render_template('homeTemplates/index.html')


@home.route('/')
def Index():
    return render_template('homeTemplates/index.html')
