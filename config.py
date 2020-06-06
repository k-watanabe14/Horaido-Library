import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
#    SQLALCHEMY_DATABASE_URI = os.environ['postgres://njzwcgxdutwzqw:cade87b0e09a2aa89e321684154e141168a57b51eb76a5d745461f55fdf3bb1d@ec2-3-222-150-253.compute-1.amazonaws.com:5432/d46uivod9p6oqd']

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True