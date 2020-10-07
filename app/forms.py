from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import MultiCheckboxField

# from wtforms.validators import InputRequired

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

class URL_Add(FlaskForm):

    url_long = StringField("URL (Original)", default=None)#, validators=[InputRequired()])
    add = SubmitField("Add")

class URL_Delete(FlaskForm):
    url_short = MultiCheckboxField("URL (Shortened)")
    delete = SubmitField("Delete")
