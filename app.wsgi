import sys
sys.path.insert(0, "/var/www/flask-app")

activate_this = "/home/muhmad/.local/share/virtualenvs/flask-app-yYmzn1cG/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application