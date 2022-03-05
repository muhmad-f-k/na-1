from flask import Flask
from dinner.routes import dinner
from groups.routes import groups
from home.routes import home
from recipe.routes import recipe
from users.users_routes import users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrbean'
app.register_blueprint(dinner)
app.register_blueprint(home)
app.register_blueprint(groups)
app.register_blueprint(recipe)
app.register_blueprint(users)
if __name__ == '__main__':
    app.run(debug=True)
