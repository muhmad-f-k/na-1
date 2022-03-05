from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import MakeDinnerForm,\
    UpdateDinnerForm, DeleteDinnerForm, MakeMealForm, UpdateMealForm, DeleteMealForm

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
        flash(f'Middag {form.mp_dinner_title.data} opprettet!')
        # UTKAST TIL DATABASE-LOGIKK
        # mp_dinner = Dinner(mp_name=form.mp_dinner_title, mp_image=form.mp_dinner_image)
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
        #        where(Dinner.mp_dinner_id == form.mp_dinner_id.data).
        #        values(mp_dinner_title=form.mp_dinner_title.data,
        #               mp_dinner_image=form.mp_dinner_image.data)
        #)
        # db.commit()
        flash(f'Middag {form.mp_dinner_id.data} oppdatert!')
    return render_template('updateDinner.html', form=form)


@dinner.route('/deleteDinner', methods=['GET', 'POST'])
def delete_dinner():
    form = DeleteDinnerForm()
    if form.validate_on_submit():
        #userId = db.session.get(Dinner, form.mp_dinner_id.data)
        #db.session.delete(userId)
        #db.session.commit()
        flash(f'Middag {form.mp_dinner_id.data} slettet!')
    return render_template('deleteDinner.html', form=form)



@dinner.route('/makeMeal', methods=['GET', 'POST'])
def make_meal():
    form = MakeMealForm()
    if form.validate_on_submit():
        flash(f'Middag {form.mp_dinner_mp_dinner_id.data} lagt til dato {form.mp_meal_date.data}!')
    return render_template('makeMeal.html', form=form)


@dinner.route('/updateMeal', methods=['GET', 'POST'])
def update_meal():
    form = UpdateMealForm()
    if form.validate_on_submit():
        flash(f'Middag {form.mp_dinner_mp_dinner_id.data} lagt til / flyttet til dato {form.mp_meal_date.data}!')
    return render_template('updateMeal.html', form=form)


@dinner.route('/deleteMeal', methods=['GET', 'POST'])
def delete_meal():
    form = DeleteMealForm()
    if form.validate_on_submit():
        flash(f'Middag på dato {form.mp_meal_date.data} slettet!')
    return render_template('deleteMeal.html', form=form)
