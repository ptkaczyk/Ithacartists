from flask import render_template, Flask, flash
from app import app
from app.forms import artistForm



@app.route('/')
@app.route('/landing')
def landing():
    return render_template('Landing.html',title='Landing')


@app.route('/artistlist')
def artistlist():

    displayedartists = [
        {'name': 'Jim and friends'}, {'name': 'People with Beards'}, {'name': 'No More Hats'},
        {'name': 'The Musketeers'}
    ]
    return render_template('Artists.html', displayedartists=displayedartists,title='Artists')


@app.route('/newartist', methods=['GET', 'POST'])
def newartist():
    form = artistForm()
    if form.validate_on_submit():
        flash('New page created: {}'.format(form.artistName.data))
        return render_template('Artist.html', title='Artist', artistName=form.artistName.data, hometown=form.hometown.data, description=form.description.data)
    return render_template('NewArtist.html', form=form, title='New Artist')


@app.route('/artist')
def artist():
    return render_template('Artist.html', title='Artist', artistName='People With Beards', hometown='Ithaca', description='People With Beards was founded in 1933 to advance the cause of beards.')