from flask import render_template, Flask, flash, redirect, url_for, abort, request
from flask_login import login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import artistForm, loginForm, registerForm, eventForm, venueForm
from app.models import *



@app.route('/')
@app.route('/landing')
def landing():
    return render_template('Landing.html',title='Landing')


@app.route('/artistlist')
def artistlist():
    artists=Artist.query.all()
    return render_template('Artists.html', artists=artists, title='Artists')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect name or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('landing'))
    return render_template('Login.html', form=form, title='Login')

@app.route('/newartist', methods=['GET', 'POST'])
@login_required
def newartist():
    form = artistForm()
    if form.validate_on_submit():
        if len(Artist.query.filter_by(firstname=form.artistName.data).all()) > 0:
            flash('That name already exists')
        else:
            flash('New page created: {}'.format(form.artistName.data))
            newA = Artist(firstname=form.artistName.data, lastname='', hometown=form.hometown.data, description=form.description.data)
            db.session.add(newA)
            db.session.commit()
            return redirect(url_for('artistlist'))
    return render_template('NewArtist.html', form=form, title='New Artist')

@app.route('/newvenue', methods=['GET','POST'])
def newvenue():
    form = venueForm()
    if form.validate_on_submit():
        if len(Venue.query.filter_by(name=form.name.data).all()) > 0:
            flash('That venue already exists')
        else:
            flash('New venue created: {}'.format(form.name.data))
            newV = Venue(name=form.name.data, description=form.description.data)
            db.session.add(newV)
            db.session.commit()
            return redirect(url_for('artistlist'))
    return render_template('NewVenue.html', title='New Venue', form=form)

@app.route('/newevent', methods=['GET', 'POST'])
def newevent():
    form = eventForm()
    form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.all()]
    form.artists.choices = [(artist.id, artist.firstname) for artist in Artist.query.all()]
    if form.validate_on_submit():
        if len(Event.query.filter_by(name=form.name.data).all()) > 0:
            flash('That event already exists')
        else:
            flash('New event created: {}'.format(form.name.data))
            newE = Event(name=form.name.data, description=form.description.data, time=form.time.data, venueId=form.venue.data)
            db.session.add(newE)
            db.session.commit()
            for a in form.artists.data:
                newX = ArtistToEvent(artistId=Artist.query.filter_by(id=a).first().id, eventId=newE.id)
                db.session.add(newX)
                db.session.commit()
            return redirect(url_for('artistlist'))
    return render_template('NewEvent.html', title='New Event', form=form)


@app.route('/artist/<name>')
#instructor = Instructor.query.filter_by(firstname="Alex").first()
def artist(name):
    if len(Artist.query.filter_by(firstname=name).all()) > 0:
        chosenArtist=Artist.query.filter_by(firstname=name).first()
        chosenJoins=ArtistToEvent.query.filter_by(artistId=chosenArtist.id).all()
        chosenEvents = []
        trackingInt=0
        for oneEvent in chosenJoins:
            chosenEvents.append(Event.query.filter_by(id=chosenJoins[trackingInt].eventId).first())
            trackingInt=trackingInt+1
        #chosenEvents=Event.query.filter_by(id=chosenJoin.eventId).all()
        return render_template('Artist.html', title='Artist', artistName=chosenArtist.firstname, hometown=chosenArtist.hometown, description=chosenArtist.description, event_list=chosenEvents)
    else:
        abort(404)

@app.route('/register', methods=['GET','POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        if len(User.query.filter_by(username=form.username.data).all()) > 0:
            flash('That name already exists')
        else:
            flash('New user created. You can now log in.')
            newU= User(username=form.username.data, password=form.password.data)
            newU.set_password(form.password.data)
            db.session.add(newU)
            db.session.commit()
            return redirect(url_for('landing'))
    return render_template('Register.html', form=form, title='Register')

@app.route('/logout')
def logout():
    logout_user()
    flash("User has been logged out.")
    return redirect(url_for('landing'))

@app.route('/populate_db')
def populate_db():

    a1=Artist(firstname='Anne', lastname='Apricot', hometown='Ithaca', description='A')
    a2=Artist(firstname='Ben', lastname='Barrel', hometown='Ithaca', description='B')
    a3=Artist(firstname='Cathy', lastname='Chowder', hometown='Ithaca', description='C')
    a4=Artist(firstname='Dan', lastname='Derringer', hometown='Delanson', description='D')

    e1=Event(name='Augustfest', description='A', venueId='0')
    e2 = Event(name='Burgerfest', description='B', venueId='1')
    e3 = Event(name='Ciderfest', description='C', venueId='2')
    e4 = Event(name='Donutfest', description='D', venueId='1')
    e5 = Event(name='Earwigfest', description='E', venueId='1')
    e6 = Event(name='Falafelfest', description='F', venueId='2')

    ate1 = ArtistToEvent(artistId=1, eventId=1)
    ate2 = ArtistToEvent(artistId=2, eventId=2)
    ate3 = ArtistToEvent(artistId=3, eventId=3)
    ate4 = ArtistToEvent(artistId=4, eventId=4)
    ate5 = ArtistToEvent(artistId=1, eventId=5)
    ate6 = ArtistToEvent(artistId=2, eventId=5)
    ate7 = ArtistToEvent(artistId=3, eventId=6)
    ate8 = ArtistToEvent(artistId=1, eventId=6)

    v1=Venue(name='Adelide Acres', description='A')
    v2 = Venue(name='Baltimore Barrelers', description='B')
    v3 = Venue(name='Canary Church', description='C')

    u1 = User(username='Peter',password='Tkaczyk')
    u1.set_password('Tkaczyk')

    db.session.add_all([a1,a2,a3,a4,ate1,ate2,ate3,ate4,ate5,ate6,ate7,ate8,e1,e2,e3,e4,e5,e6,v1,v2,v3,u1])
    db.session.commit()
    return "database has been populated."

@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()
   populate_db()
   return "Reset and repopulated data."