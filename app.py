from flask import Flask
from dinner.routes import dinner
#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrbean'
app.register_blueprint(dinner)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
