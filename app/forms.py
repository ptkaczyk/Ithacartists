from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class artistForm(FlaskForm):
    artistName = StringField('Name',validators=[DataRequired()])
    hometown = StringField('Hometown',validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class registerForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class venueForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')

class eventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    time = DateField('Time',format='%Y-%m-%d')
    venue = SelectField(u'Venue', coerce=int)
    artists = SelectMultipleField(u'Artists', coerce=int)
    submit = SubmitField('Submit')

