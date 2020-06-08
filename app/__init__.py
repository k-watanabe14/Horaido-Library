import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


# Import a module / component using its blueprint handler
from app.auth.controllers import mod_auth
from app.register.controllers import mod_register

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_register)


if __name__ == '__main__':
    app.run()
