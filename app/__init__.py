from flask import Flask, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
#app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

from app.routes import *