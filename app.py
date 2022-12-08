"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'tacosandburritos'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.get('/')
def home():
    """ redirects to to users page"""
    return redirect('/users')

@app.get('/users')
def users():
    """ returns users page with list of users"""
    users = User.query.all()

    return render_template('users.html', users = users)

@app.get('/users/new')
def new_user():
    """ returns new user page with form for adding a user"""

    return render_template('new_user_form.html')

@app.post('/users/new')
def add_new_user():
    """ posts new user form data and redirects to users"""

    first = request.form['first-name']
    last = request.form['last-name']
    img_url = request.form['img-url'] or None #if img-url is empty then it will use None

    new_user = User(first_name=first, last_name=last, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    flash("User Successfully Added!")

    return redirect('/users')

@app.get('/users/<int:user_id>')
def get_user_by_id(user_id):
    """ returns specific user page and populates with user data"""

    user = User.query.get(user_id)

    return render_template('user_detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """ returns edit user page given the user_id variable"""
    user = User.query.get(user_id)

    return render_template('edit_user.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """ posts edited user data and redirects to that user's page with edited data"""

    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url= request.form['img-url']

    db.session.add(user)
    db.session.commit()

    flash("User Successfully Edited!")

    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ deletes user at user_id argument and redirects to users page"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User Successfully Edited!")

    return redirect('/users')

