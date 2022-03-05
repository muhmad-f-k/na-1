from flask import request
from sqlalchemy import update

from modul import *


def db_new_dinner(mp_dinner_title, mp_dinner_image):
    dinner = Dinner(title=mp_dinner_title, image=mp_dinner_image)
    session.add(dinner)
    session.commit()


def db_update_dinner(mp_dinner_id, mp_dinner_title, mp_dinner_image):
    incoming_dinner = session.query(Dinner).filter(Dinner.id == mp_dinner_id).first()
    incoming_dinner.title = mp_dinner_title
    incoming_dinner.image = mp_dinner_image
    session.commit()
