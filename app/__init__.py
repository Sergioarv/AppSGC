from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
#app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('config.TestConfig')

email_emp = app.config['MAIL_USERNAME']
password_emp = app.config['MAIL_PASSW']

db = SQLAlchemy(app)

from app.routes import myrequest, dashboard, flyer, quotation, survey