from flask import Flask
from flask_login import LoginManager
from db.modul import session, User
from routes.ingredient_routes import ingredientroute
from routes.calendar_routes import calendarroute
from routes.group_routes import grouproute
from routes.recipe_routes import recipe_route
from routes.auth_routes import usersroute
from routes.edit_users_routes import edituserroute
from routes.rapport_routes import rapportroute

app = Flask(__name__)
app.config["SECRET_KEY"] = "TEST"
app.register_blueprint(usersroute)
app.register_blueprint(ingredientroute)
app.register_blueprint(calendarroute)
app.register_blueprint(grouproute)
app.register_blueprint(recipe_route)
app.register_blueprint(edituserroute)
app.register_blueprint(rapportroute)
login_manager = LoginManager()
login_manager.login_view = 'usersroute.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    user = session.query(User).get(int(id))
    session.close()
    return user


if __name__ == "__main__":
    app.run(debug=True)
