from flask import render_template
from app import app


@app.route('/')
@app.route('/landing')
def landing():
    return render_template('Landing.html')


@app.route('/artistlist')
def artistlist():

    displayedartists = [
        {'name': 'Jim and friends'}, {'name': 'People with Beards'}, {'name': 'No More Hats'},
        {'name': 'The Musketeers'}
    ]
    return render_template('Artists.html', displayedartists=displayedartists)


@app.route('/newartist')
def newartist():
    return render_template('NewProduct.html')


@app.route('/artist')
def artist():
    return render_template('Artist.html')