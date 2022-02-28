from flask import Flask

from dinner.routes import dinner


def create_app():
    app = Flask(__name__)

    app.register_blueprint(dinner)

    return app
