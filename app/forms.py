from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class artistForm(FlaskForm):
    artistName = StringField('Name',validators=[DataRequired()])
    hometown = StringField('Hometown',validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')

