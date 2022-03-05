from flask import Flask
from recipe.routes import recipe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jonis'
app.register_blueprint(recipe)

if __name__ == '__main__':
    app.run(debug=True)