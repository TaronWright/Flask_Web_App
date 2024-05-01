from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default = func.now() )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreignkey must have the primary key of the reference data (in lowercase)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) #primary key is the database object unique identifier
    email = db.Column(db.String(150), unique = True) # unique = True means no two objects in database can share this value
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note') # creates a relationship with the note table

    