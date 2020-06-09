import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.auth.controllers import login_required

@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Import a module / component using its blueprint handler
from app.auth.controllers import mod_auth
from app.account.controllers import mod_account
from app.search.controllers import mod_search
from app.register.controllers import mod_register
from app.borrow.controllers import mod_borrow
from app.return_.controllers import mod_return

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_account)
app.register_blueprint(mod_search)
app.register_blueprint(mod_register)
app.register_blueprint(mod_borrow)
app.register_blueprint(mod_return)


if __name__ == '__main__':
    app.run()
