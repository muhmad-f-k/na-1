from flask import Blueprint, render_template, flash, url_for, redirect
from dinner.forms import MakeDinnerForm, \
    UpdateDinnerForm, DeleteDinnerForm, MakeMealForm, UpdateMealForm, DeleteMealForm
from dinner.queries import *

dinner = Blueprint('dinner', __name__)


@dinner.route('/makeDinner', methods=['GET', 'POST'])
def make_dinner():
    form = MakeDinnerForm()
    if form.validate_on_submit():
        if form.mp_dinner_image.data:
            content = form.mp_dinner_image.data.read()
            db_new_dinner(form.mp_dinner_title.data, form.mp_dinner_user_id.data, form.mp_dinner_group_id.data, content)
        else:
            db_new_dinner(form.mp_dinner_title.data, form.mp_dinner_user_id.data, form.mp_dinner_group_id.data, None)
        flash(f'Middag {form.mp_dinner_title.data} opprettet!')
    return render_template('dinnertamplates/makeDinner.html', form=form)


@dinner.route('/updateDinner', methods=['GET', 'POST'])
def update_dinner():
    form = UpdateDinnerForm()
    if form.validate_on_submit():
        if form.mp_dinner_image.data:
            content = form.mp_dinner_image.data.read()
            db_update_dinner(form.mp_dinner_id.data, form.mp_dinner_title.data,
                             form.mp_dinner_user_id.data, form.mp_dinner_group_id.data, content)
        else:
            db_update_dinner(form.mp_dinner_id.data, form.mp_dinner_title.data,
                             form.mp_dinner_user_id.data, form.mp_dinner_group_id.data, None)
        flash(f'Middag {form.mp_dinner_id.data} oppdatert!')
    return render_template('dinnertamplates/updateDinner.html', form=form)


@dinner.route('/deleteDinner', methods=['GET', 'POST'])
def delete_dinner():
    form = DeleteDinnerForm()
    if form.validate_on_submit():
        db_delete_dinner(form.mp_dinner_id.data)
        flash(f'Middag {form.mp_dinner_id.data} slettet!')
    return render_template('dinnertamplates/deleteDinner.html', form=form)


@dinner.route('/makeMeal', methods=['GET', 'POST'])
def make_meal():
    form = MakeMealForm()
    if form.validate_on_submit():
        db_new_meal(form.mp_meal_date.data, form.mp_dinner_mp_dinner_id.data)
        flash(f'Middag {form.mp_dinner_mp_dinner_id.data} lagt til dato {form.mp_meal_date.data}!')
    return render_template('dinnertamplates/makeMeal.html', form=form)


@dinner.route('/updateMeal', methods=['GET', 'POST'])
def update_meal():
    form = UpdateMealForm()
    if form.validate_on_submit():
        db_update_meal(form.mp_meal_id.data, form.mp_meal_date.data, form.mp_dinner_mp_dinner_id.data)
        flash(f'Middag {form.mp_dinner_mp_dinner_id.data} lagt til / flyttet til dato {form.mp_meal_date.data}!')
    return render_template('dinnertamplates/updateMeal.html', form=form)


@dinner.route('/deleteMeal', methods=['GET', 'POST'])
def delete_meal():
    form = DeleteMealForm()
    if form.validate_on_submit():
        db_delete_meal(form.mp_meal_date.data)
        flash(f'Middag på dato {form.mp_meal_date.data} slettet!')
    return render_template('dinnertamplates/deleteMeal.html', form=form)

@dinner.route('/dinnerlinks')
def dinner_links():
    return render_template('dinnertamplates/dinnerlinks.html')

@dinner.route('/dinner')
def dinner_linkes():
    return render_template('dinnertamplates/dinnerlinks.html')