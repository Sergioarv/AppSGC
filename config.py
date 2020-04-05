import os

DBURL = 'sqlite:///'+ os.path.abspath('./dbsgc.db')

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mysecretkey'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DBURL
    SECRET_KEY = os.environ.get('SECRET_KEY', '920812')

class DevelopmentConfig(Config):
    DEBUG = True