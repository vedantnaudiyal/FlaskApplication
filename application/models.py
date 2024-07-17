from . import db

from flask_login import UserMixin

class Employee(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    age=db.Column(db.Integer())
    isActive=db.Column(db.Boolean(), default=True)