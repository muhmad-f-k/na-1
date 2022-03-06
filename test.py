from modul import *

# jonathan = User(email="jonathan@skaue.com", password="test123", first_name="Jonathan", last_name="Skaue")
# admin = Role(name="admin")
# gruppe = Group(name="skaue")
#
# carbonara = Dinner(title="Carbonara", group_id="1", user_id="1")

carbonaraRecipe = Recipe(approach="Hva skjer", version="1", dinner_id="1")
session.add(carbonaraRecipe)
session.commit()

