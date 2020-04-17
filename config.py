import os

# Base en Produccion Online
DBURL = 'postgres://vmrcezxgjwbrpt:90d2fa1f9c1c70555d59405d8d86d59739b91a32b92810e6675c6d6ec1ddc898@ec2-52-201-55-4.compute-1.amazonaws.com:5432/d7daj79bdhcjoi'

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.abspath('./dbsgc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mysecretkey'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DBURL
    SECRET_KEY = os.environ.get('SECRET_KEY', '920812')

class DevelopmentConfig(Config):
    DEBUG = True