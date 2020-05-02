from app import db
#from sqlalchemy.orm import relationship

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Flyer(db.Model):
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
    quotation = db.relationship('Quotation', uselist = False)

class Quotation(db.Model):
    __tablename__ = 'Quotation'
    id = db.Column(db.Integer, primary_key=True)
    para = db.Column(db.String(100), nullable=False)
    asunto = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    valueT = db.Column(db.Integer)
    hourO = db.Column(db.String(50))
    dateO = db.Column(db.String(50))
    request_id = db.Column(db.Integer, db.ForeignKey('Request.id'))
    request = db.relationship('Request')
    constrainr = db.relationship('Constraint', uselist = False)

class Constraint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    constraint = db.Column(db.String(100), nullable=False)
    tipe = db.Column(db.Integer, nullable=False)
    quotation_id = db.Column(db.Integer, db.ForeignKey('Quotation.id'))
    quotation = db.relationship('Quotation')

class Survey(db.Model):
    __tablename__ = 'Survey'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    quests = db.relationship('Question', lazy = 'dynamic')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.String(100))
    survey_id = db.Column(db.Integer, db.ForeignKey('Survey.id'))
    survey = db.relationship('Survey')