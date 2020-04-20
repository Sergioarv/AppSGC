from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Flyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(255))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    dateI = db.Column(db.String(50))
    dateO = db.Column(db.String(50))
    hourI = db.Column(db.String(50))
    hourO = db.Column(db.String(50))