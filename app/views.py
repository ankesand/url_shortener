from app import app
from app import session

from flask import render_template, redirect #, request, url_for
from sqlalchemy import asc

from datetime import datetime
from random import randint

from app.models import URL
from app.forms import URL_Add, URL_Delete

def url_short_generator():

    short_url = chr(randint(48, 57)) + chr(randint(65, 90)) + chr(randint(97, 122))

    if short_url in [row.url_short for row in session.query(URL).all()]:
        short_url_generator()
    else:
        return short_url

@app.route("/", methods=["GET", "POST"])
@app.route("/url_shortener", methods=["GET", "POST"])
def url_shortener():

    title = "ankesand.com | url_shortener"
    
    # generate forms
    
    url_add = URL_Add()
    url_delete = URL_Delete()

    # retreive existing urls
    
    urls = session.query(URL).order_by(asc(URL.added))
    url_delete.url_short.choices = [(url.url_short, url.url_short) for url in urls]
    
    # abc = session.query(URL).first()

    # post - add url_long

    if url_add.url_long.data and url_add.validate_on_submit():

        url_long_add = url_add.url_long.data

        try:

            url_short_add = url_short_generator()

            session.add(URL(url_short_add, url_long_add, datetime.now()))
            session.commit()

            url_add.url_long.data = None
            url_delete = URL_Delete()
            urls = session.query(URL).order_by(asc(URL.added))
            url_delete.url_short.choices = [(url.url_short, url.url_short) for url in urls]

            error_add = None

        except:

            session.rollback()

            error_add = "Could not add: " + url_long_add

        return render_template("url_shortener.html", title = title, url_add = url_add, url_delete = url_delete, urls = urls,
                               url_short_add = url_short_add, url_long_add = url_long_add,
                               error_add = error_add)

    # post - delete url_short

    if url_delete.url_short.data and url_delete.validate_on_submit():

        url_short_deletes = url_delete.url_short.data

        try:

            session.query(URL).filter(URL.url_short.in_(url_short_deletes)).delete(synchronize_session='fetch')
            session.commit()

            url_delete = URL_Delete()
            urls = session.query(URL).order_by(asc(URL.added))
            url_delete.url_short.choices = [(url.url_short, url.url_short) for url in urls]

            error_delete = None

        except:

            session.rollback()
            error_delete = "Could not delete: " + str(url_short_deletes)
            
        return render_template("url_shortener.html", title = title, url_add = url_add, url_delete = url_delete, urls = urls,
                               url_short_deletes = url_short_deletes,
                               error_delete = error_delete)
    
    # [else (get)]
    
    return render_template("url_shortener.html", title = title, url_add = url_add, url_delete = url_delete, urls = urls)

@app.route("/url/<url_short>")
def url_redirect(url_short):

    url_long = session.query(URL).filter(URL.url_short == url_short).one().url_long

    return redirect(url_long, code=302)
