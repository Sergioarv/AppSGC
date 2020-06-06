import os

# Base en Produccion Online
DBURL = 'postgres://yzubujzmwvbekx:e2c0d5e629709e662870395f8319a687488a5bcec8ce6d7b8f2a6a915385eba0@ec2-18-232-143-90.compute-1.amazonaws.com:5432/d1gbqo3l69tins'

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.abspath('./dbsgc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mysecretkey'
    MAIL_USERNAME = 'reservas.lacasadelturismo@gmail.com'
    MAIL_PASSW = 'oabrzpafnwphzbok'

class TestConfig(Config):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI =  'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DBURL
    SECRET_KEY = os.environ.get('SECRET_KEY', '920812')

class DevelopmentConfig(Config):
    DEBUG = True