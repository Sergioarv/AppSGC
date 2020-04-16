from app import db

class Flyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
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