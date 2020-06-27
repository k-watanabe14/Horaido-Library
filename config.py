import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://USER:PASSWORD@HOST:5432/DBNAME'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://USER:PASSWORD@HOST:5432/DBNAME'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://USER:PASSWORD@HOST:5432/DBNAME'
    BONSAI_URL = 'https://fcx4uju5en:bh5fqfi904@apple-701096738.us-east-1.bonsaisearch.net:443'

class TestingConfig(Config):
    TESTING = True