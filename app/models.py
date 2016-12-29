#
# Author: Kireet Agrawal, Pep Talk
#
from app import app, db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(100))
    goals = db.relationship('Goal', backref = 'author', lazy='dynamic')

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def getGoals(self):
        return Goal.query.filter_by(user_id = self.id).order_by(Goal.order.asc())

    def __repr__(self):
        return '<User {}>'.format(self.lastname)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    youtubeURL = db.Column(db.String(150))
    order = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, timestamp, user_id, description, youtubeURL, order):
        self.title = title
        self.timestamp = timestamp
        self.user_id = user_id
        self.description = description
        self.youtubeURL = youtubeURL
        self.order = order

    def __repr__(self):
        return '<Goal {}>'.format(self.title)

# class AnonUser(db.Model):å
#     id = db.Column(db.Integer, primary_key = True)
#     anonid = db.Column(db.String(54), index = True, unique = True)

#     def __init__(self, anonid):
#         self.anonid = anonid

#     def get_anonid(self):
#         return self.anonid

    