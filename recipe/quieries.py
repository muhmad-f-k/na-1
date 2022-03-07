from modul import *

def db_new_recipe(mp_dinner_title, mp_dinner_user_id, mp_dinner_group_id, mp_dinner_image):
    dinner = Dinner(title=mp_dinner_title, user_id=mp_dinner_user_id, group_id=mp_dinner_group_id, image=mp_dinner_image)
    session.add(dinner)
    session.commit()
    session.close()