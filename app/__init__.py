from flask import Flask
from dinner.routes import *
from groups.routes import *
from home.routes import *
from recipe.routes import *
from users.routes import *
from comment.routes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrbean'
app.register_blueprint(dinner)
app.register_blueprint(groups)
app.register_blueprint(home)
app.register_blueprint(recipe)
app.register_blueprint(users)
app.register_blueprint(comment)
