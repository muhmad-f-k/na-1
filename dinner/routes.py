from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import MakeDinnerForm

dinner = Blueprint('dinner', __name__)


# !! PLACEHOLDER KLASSE, SLETT NÅR ORDENTLIG DATABSE ER OPPRETTET !!
#class Dinner:
#    id = 1
#    mp_name = None
#    mp_date = None
#    mp_image = None


@dinner.route('/makeDinner', methods=['GET', 'POST'])
def index():
    form = MakeDinnerForm()
    if form.validate_on_submit():
        flash(f'Middag {form.mp_name.data} opprettet!')
        # UTKAST TIL DATABASE-LOGIKK
        # mp_dinner = Dinner(mp_name=form.mp_name, mp_date=form.mp_date, mp_image=form.mp_image)
        # db.session.add(mp_dinner)
        # db.commit()
    # print(form.errors)
    return render_template('makeDinner.html', form=form)
