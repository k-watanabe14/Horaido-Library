import os
import tempfile

import pytest

from app import app
from app.auth import login, logout

@pytest.fixture
def client():
    db_fd  = tempfile.mkstemp()
    app.config.from_object('config.TestingConfig')

    with app.test_client() as client:
        yield client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

# TODO: Make Unit Tests
def test_login_logout(client):
    """Make sure login and logout works."""

    # rv = login(client, 'わたなべ', '12345678')
    # assert b'You were logged in' in rv.data

    # rv = logout(client)
    # assert b'You were logged out' in rv.data

    # rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    # assert b'Invalid username' in rv.data

    # rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    # assert b'Invalid password' in rv.data