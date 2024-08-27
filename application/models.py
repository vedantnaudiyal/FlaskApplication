from . import db
from datetime import date
from sqlalchemy import event
from flask_login import UserMixin

now=date.today()

class Employee(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    age=db.Column(db.Integer())
    isActive=db.Column(db.Boolean(), default=True)
    dateofjoining=db.Column(db.Date, default=now)

    def generate_email(self):
        return f"{self.name.split(' ')[0]}@gmail.com"


@event.listens_for(Employee, 'before_insert')
def set_default_email(mapper, connection, target):
    print("email", target)
    if not target.email:
        target.email=target.generate_email()
        print(target.email)



