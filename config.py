import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://njzwcgxdutwzqw:cade87b0e09a2aa89e321684154e141168a57b51eb76a5d745461f55fdf3bb1d@ec2-3-222-150-253.compute-1.amazonaws.com:5432/d46uivod9p6oqd'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://jtwxhkhlqfawzi:ee6255feb4d01b03bc067a8aea5e370a59d21d2d859b5e61abb95e99f396658f@ec2-54-86-170-8.compute-1.amazonaws.com:5432/ddgbjlbb55ob6s'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:123456@localhost/houraidou'

class TestingConfig(Config):
    TESTING = True