from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dinner.routes import dinner
from recipe.routes import recipe
from comment.routes import comment
#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrbean'
app.register_blueprint(dinner)
app.register_blueprint(recipe)
app.register_blueprint(comment)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
