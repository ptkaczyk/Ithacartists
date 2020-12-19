from flask import render_template, Flask, flash, redirect, url_for, abort, request
from flask_login import login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import *
from app.models import *


@app.route('/')
@app.route('/landing')
def landing():
    return render_template('Landing.html', title='Landing')


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


@app.route('/search', methods=['GET','POST'])
def search():
    searched = Product.query.all()
    form = searchForm()
    if form.validate_on_submit():
        searched = Product.query.filter_by(name=form.searchable.data).all()
    return render_template('search.html', searchable=searched, form=form, title='Search')


@app.route('/user/<name>')
def user(name):
   if len(User.query.filter_by(username=name).all()) > 0:
       chosenUser = User.query.filter_by(username=name).first()
       chosenProducts = Product.query.filter_by(Id=chosenUser.id).all()
       return render_template('user.html', title='User', userName=chosenUser.username, chosenUser=chosenUser,
                              productList=chosenProducts)
   else:
       abort(404)


@app.route('/product/<productName>')
def product(productName):
   if len(Product.query.filter_by(name=productName).all()) > 0:
       chosenProduct=Product.query.filter_by(name=productName).first()
       chosenUser=User.query.filter_by(id=chosenProduct.userId).first()
       userName=chosenUser.username
       return render_template('product.html', title='Product', name=productName, userPosting=userName,
                              description=chosenProduct.description, date=chosenProduct.dateHarvested,
                              productPrice=chosenProduct.price, amount=chosenProduct.amount)
   else:
       abort(404)


@app.route('/newProduct', methods=['GET','POST'])
def newProduct():
   form = productForm()
   if form.validate_on_submit():
        flash('New product created: {}'.format(form.name.data))
        newP = Product(name=form.name.data, description=form.description.data, price=form.price.data, amount=form.amount.data, dateHarvested=form.date.data, userId=4)
        db.session.add(newP)
        db.session.commit()
        return redirect(url_for('landing'))
   return render_template('newProduct.html', title='New Product', form=form)


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

    v1 = Venue(name='Adelide Acres', description='A')
    v2 = Venue(name='Baltimore Barrelers', description='B')
    v3 = Venue(name='Canary Church', description='C')

    u1 = User(username='Peter',password='Tkaczyk')
    u1.set_password('Tkaczyk')
    u2 = User(username='Old Man McFarmer', password='Farmlivin')
    u2.set_password('Farmlivin')
    u3 = User(username='Young Man McFarmer', password='ILovFarm')
    u3.set_password('ILovFarm')

    p1 = Product(name='Eggs', amount = 12, dateHarvested = '12-12-2020', description = 'delicious eggs', price = '$0.99'
                 , userId=1)
    p2 = Product(name='Tomatoes', amount=20, dateHarvested='12-14-2020', description='delicious tomatoes', price='$1.99',
                  userId=2)
    p3 = Product(name='Beets', amount=30, dateHarvested='12-10-2020', description='delicious beets', price='$2.99'
                 , userId=3)
    p4 = Product(name='Bacon', amount=10, dateHarvested='11-20-2020', description='delicious bacon', price='$3.99',
                  userId=2)
    p5 = Product(name='Turnips', amount=40, dateHarvested='12-10-2020', description='delicious turnips', price='$4.99',
                 userId=3)

    db.session.add_all([u1, u2, u3, p1, p2, p3, p4, p5])
    db.session.commit()
    return "database has been populated."


@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()
   populate_db()
   return "Reset and repopulated data."
