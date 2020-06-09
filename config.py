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
    SQLALCHEMY_DATABASE_URI = 'postgres://loydczttqhkyxg:b566b9863c0e45648712543109b794f21064e25aa39a4f4da13da60a4698335c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/dcprltrsdcm3gs'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:123456@localhost/houraidou'

class TestingConfig(Config):
    TESTING = True