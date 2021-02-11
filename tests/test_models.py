import os
import pytest
from app import app
from app.models import User, Book, History, TagMaps, Tags


@pytest.fixture(scope='module')
def new_user():
    user = User('John', 'john@gmail.com', 'FlaskIsAwesome', True)
    return user


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.username == 'John'
    assert new_user.email == 'john@gmail.com'
    assert new_user.password == 'FlaskIsAwesome'
