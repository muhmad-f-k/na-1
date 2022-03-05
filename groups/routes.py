from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from groups.forms import groupsform

groups = Blueprint('groups', __name__)


@groups.route('/groups')
def index():
    form = groupsform()
    return render_template('groups.html', form=form)
