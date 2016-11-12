from app import app, db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<User {}>'.format(self.lastname)

# class AnonUser(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     anonid = db.Column(db.String(54), index = True, unique = True)

#     def __init__(self, anonid):
#         self.anonid = anonid

#     def get_anonid(self):
#         return self.anonid

    