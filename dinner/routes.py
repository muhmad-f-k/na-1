from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import MakeDinnerForm

dinner = Blueprint('dinner', __name__)


@dinner.route('/dinner', methods=['GET', 'POST'])
def index():
    form = MakeDinnerForm()
    print(form.errors)
    if form.validate_on_submit():
        flash(f'Middag {form.dinnerName.data} opprettet!')
        flash(f'Bilde: {form.image.data}')
    print(form.errors)
    return render_template('dinner.html', form=form)
