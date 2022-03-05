from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dinner.routes import dinner
from recipe.routes import recipe
#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrbean'
app.register_blueprint(dinner)
app.register_blueprint(recipe)

if __name__ == '__main__':
    app.run(debug=True)
