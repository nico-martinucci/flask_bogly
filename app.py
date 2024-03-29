"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'tacosandburritos'

# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.get('/')
def home():
    """ Redirects to to users page"""
    return redirect('/users')

@app.get('/users')
def users():
    """ Returns users page with list of users"""
    users = User.query.all()

    return render_template('users.html', users = users)

@app.get('/users/new')
def new_user():
    """ Returns new user page with form for adding a user"""

    return render_template('new_user_form.html')

@app.post('/users/new')
def add_new_user():
    """ Posts new user form data and redirects to users"""

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
    """ Returns specific user page and populates with user data"""

    user = User.query.get(user_id)

    return render_template('user_detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """ Returns edit user page given the user_id variable"""
    user = User.query.get(user_id)

    return render_template('edit_user.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """ Posts edited user data and redirects to that user's page with edited data"""

    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url= request.form['img-url']

    db.session.commit()

    flash("User Successfully Edited!")

    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Deletes user at user_id argument and redirects to users page"""
    user = User.query.get(user_id)
    posts = user.posts

    db.session.delete(user)

    for post in posts:
        db.session.delete(post)

    db.session.commit()

    flash("User Successfully Deleted!")

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """ Show form to create new post """
    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template('new_post.html', user = user, tags = tags)

@app.post('/users/<int:user_id>/posts/new')
def submit_new_post(user_id):
    """ Submit form data from new post """
    title = request.form['title']
    content = request.form['content']
    tags_list = request.form.getlist('tags')


    new_post = Post(title = title , content = content, user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags_list:
        temp_tag = Tag.query.filter(Tag.name == tag).one()
        breakpoint()
        new_post.tags.append(temp_tag)
        db.session.commit()

    flash("Post Successfully Added!")
    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def display_post(post_id):
    """ Display post given the post_id argument """
    post = Post.query.get(post_id)

    return render_template('post_detail.html', post = post)

@app.get('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """ Display edit post page given post_id argument"""

    post = Post.query.get(post_id)

    return render_template('edit_post.html', post = post)

@app.post('/posts/<int:post_id>/edit')
def submit_edit_post(post_id):
    """ Submit form data to edit existing post"""
    edited_post = Post.query.get(post_id)
    edited_post.title = request.form['title']
    edited_post.content = request.form['content']

    db.session.commit()

    flash("Post Successfully Edited!")
    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """ Delete post given the post_id argument"""
    post = Post.query.get(post_id)
    user_id = post.author.id
    db.session.delete(post)
    db.session.commit()

    flash("Post Successfully Deleted!")
    return redirect(f'/users/{user_id}')

@app.get('/tags')
def display_tags():
    """ Display tags page with list of current tags"""
    tags = Tag.query.all()

    return  render_template('tags.html', tags = tags)

@app.get('/tags/new')
def show_new_tag_form():
    """ Show form page for creating a new tag """

    return render_template('add_tag.html')

@app.post('/tags/new')
def create_new_tag():
    """ Pull tag from form and create new tag in database """

    tag_name = request.form['tag']
    try:
        new_tag = Tag(name = tag_name)
        db.session.add(new_tag)
        db.session.commit()

        flash('Tag successfully added!')
        return redirect('/tags')
    except:
        flash('This tag already exists. Please try another.')
        return redirect('/tags/new')



