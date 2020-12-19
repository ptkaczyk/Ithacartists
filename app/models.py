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


class Product(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    #userToLocationID = db.Column(db.Integer, db.ForeignKey('UserToLocation.id'))
    dateHarvested = db.Column(db.String(2000))
    amount = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(400), index=True)
    price = db.Column(db.String(20), index=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Product: {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    #companyName = db.Column(db.String(100), index=True)
    password = db.Column(db.String(100))
    password_hash = db.Column(db.String(400))
    Location = db.relationship("user_to_location", backref='User', lazy='dynamic')
    Product = db.relationship('Product', backref='User', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#class PaymentInfo(db.Model):
  #id=db.Column(db.Integer,primary_key=True)
  #cardType=db.Column(db.String(20), index=True)
  #cardNumber=db.Column(db.String(9), index=True)
  #securityNumber=db.Column(db.String(3))
  #userId=db.Column(db.Integer,db.ForeignKey('user.id'))

  #def __repr__(self):
  #      return '<Payment Info {}>'.format(User.query.filter_by(id=self.userId).first().firstName)


class user_to_location(db.Model):
      Id = db.Column(db.Integer, primary_key=True)
      userID = db.Column(db.Integer, db.ForeignKey('user.id'))
      locationID = db.Column(db.Integer, db.ForeignKey('location.id'))
      #Product = db.relationship("Product", backref='user to location', lazy='dynamic')

      def __repr__(self):
          return '<UserToLocation {}>'.format(self.body)


class Location(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      zipcode = db.Column(db.String(64), index=True)
      city = db.Column(db.String(64), index=True)
      state = db.Column(db.String(64), index=True)
      address = db.Column(db.String(120), index=True, unique=True)
      country = db.Column(db.String(64), index=True)
      userToLocation = db.relationship("user_to_location", backref='location', lazy='dynamic')

      def __repr__(self):
          return '<Location: {}>'.format(self.zipcode)