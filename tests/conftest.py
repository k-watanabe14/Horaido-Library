import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():

    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')

    db = SQLAlchemy(app)
    db.create_all()

    with app.app_context():
        db.engine.execute(_data_sql)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
