from flask import Flask

from wtforms import SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

app = Flask(__name__)

app.config.from_object('config')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///urls.db', connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)()

from app import views
