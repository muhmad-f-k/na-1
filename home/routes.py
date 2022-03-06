from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home = Blueprint('simple_page', __name__)


@home.route('/home')
def index():
    return render_template('homeTemplates/index.html')


@home.route('/')
def Index():
    return render_template('homeTemplates/index.html')
