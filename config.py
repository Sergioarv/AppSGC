import os

# Base en Produccion Online
DBURL = 'postgres://wviqnqyhdeqzse:c870122ac441bd00ce0c905849e29247b819822df9e07dd2f8eb01270e6f84f9@ec2-3-91-112-166.compute-1.amazonaws.com:5432/d9dh9aftbst1tp'
# Base Local
# DBURL = 'sqlite:///'+ os.path.abspath('./dbsgc.db')

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