from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Artist(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    hometown = db.Column(db.String(120), index=True)
    description = db.Column(db.String(5000))
    ArtistToEvent = db.relationship('ArtistToEvent', backref='musician', lazy='dynamic')

    def __repr__(self):
        return '<Artist {} - {} {}>'.format(self.id, self.firstname, self.lastname)

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000), index=True, unique=True)
    Events = db.relationship('Event', backref='location', lazy='dynamic')

    def __repr__(self):
       return '<Venue {} - {}>'.format(self.id, self.name)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000), index=True, unique=True)
    time = db.Column(db.String(1000))
    venueId = db.Column(db.Integer, db.ForeignKey('venue.id'))
    ArtistToEvent = db.relationship('ArtistToEvent', backref='event', lazy='dynamic')

    def __repr__(self):
        return '<Event {} - {}>'.format(self.id, self.name)

class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistId = db.Column(db.Integer, db.ForeignKey('artist.id'))
    eventId = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<ArtistToEvent {}>'.format(self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    password = db.Column(db.String(100))
    password_hash = db.Column(db.String(400))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)