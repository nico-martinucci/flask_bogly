"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.get('/')
def home():
    return redirect('/users')

@app.get('/users')
def users():
    users = User.query.all()

    return render_template('users.html', users = users)

@app.get('/users/new')
def new_user():

    return render_template('new_user_form.html')

@app.post('/users/new')
def add_new_user():

    first = request.form['first-name']
    last = request.form['last-name']
    img_url = request.form['img-url']

    new_user = User(first_name=first, last_name=last, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def get_user_by_id(user_id):

    user = User.query.get(user_id)

    return render_template('user_detail.html', user=user)


