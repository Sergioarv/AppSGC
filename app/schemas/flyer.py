from app import db

class Flyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    imagen = db.Column(db.String(255), unique=True)