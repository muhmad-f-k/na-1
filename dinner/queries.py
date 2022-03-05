from flask import request

from modul import *


def new_dinner(mp_dinner_title, mp_dinner_image):
    dinner = Dinner(title=mp_dinner_title, image=mp_dinner_image)
    session.add(dinner)
    session.commit()
