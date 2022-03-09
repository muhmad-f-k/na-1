from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from groups import *
from groups.forms import *

groups = Blueprint('groups', __name__, template_folder="templates")


@groups.route('/groups')
def index():
    form = groupsform()
    return render_template('loginTemplates/groups.html', form=form)
