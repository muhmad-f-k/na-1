from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import MakeDinnerForm, UpdateDinnerForm, DeleteDinnerForm

dinner = Blueprint('dinner', __name__)


# !! PLACEHOLDER KLASSE, SLETT NÅR ORDENTLIG DATABSE ER OPPRETTET !!
#class Dinner:
#    id = 1
#    mp_name = None
#    mp_date = None
#    mp_image = None


@dinner.route('/makeDinner', methods=['GET', 'POST'])
def make_dinner():
    form = MakeDinnerForm()
    if form.validate_on_submit():
        flash(f'Middag {form.mp_name.data} opprettet!')
        # UTKAST TIL DATABASE-LOGIKK
        # mp_dinner = Dinner(mp_name=form.mp_name, mp_date=form.mp_date, mp_image=form.mp_image)
        # db.session.add(mp_dinner)
        # db.commit()
    # print(form.errors)
    return render_template('makeDinner.html', form=form)


@dinner.route('/updateDinner', methods=['GET', 'POST'])
def update_dinner():
    form = UpdateDinnerForm()
    if form.validate_on_submit():
        # UTKAST TIL DATABASE-LOGIKK
        #stmt = (
        #    update(Dinner).
        #        where(Dinner.mp_id == form.mp_id.data).
        #        values(name=form.mp_name.data,
        #               name=form.mp_image.data)
        #)
        # db.commit()
        flash(f'Middag {form.mp_id.data} oppdatert!')
    return render_template('updateDinner.html', form=form)


@dinner.route('/deleteDinner', methods=['GET', 'POST'])
def delete_dinner():
    form = DeleteDinnerForm()
    if form.validate_on_submit():
        #userId = db.session.get(Dinner, form.mp_id.data)
        #db.session.delete(userId)
        #db.session.commit()
        flash(f'Middag {form.mp_id.data} slettet!')
    return render_template('deleteDinner.html', form=form)
