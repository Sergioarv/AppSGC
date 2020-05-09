from app import db
from sqlalchemy.orm import relationship

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Flyer(db.Model):
    __tablename__ = 'Flyer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.LargeBinary)

class Request(db.Model):
    __tablename__ = 'Request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    dateI = db.Column(db.String(50))
    hourI = db.Column(db.String(50))

class Quotation(db.Model):
    __tablename__ = 'Quotation'
    id = db.Column(db.Integer, primary_key=True)
    para = db.Column(db.String(100), nullable=False)
    asunto = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    numP = db.Column(db.Integer)
    valueT = db.Column(db.Integer)
    dateO = db.Column(db.String(50))
    hourO = db.Column(db.String(50))
    request_id = db.Column(db.Integer, unique=True)

class Constraint(db.Model):
    __tablename__ = 'Constraint'
    id = db.Column(db.Integer, primary_key=True)
    constraint = db.Column(db.String(100), nullable=False)
    tipe = db.Column(db.Integer, nullable=False)
    quotation_id = db.Column(db.Integer)

class Survey(db.Model):
    __tablename__ = 'Survey'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    quotation_id = db.Column(db.Integer, unique=True)

class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.String(100))
    answer = db.Column(db.String(100))
    survey_id = db.Column(db.Integer)