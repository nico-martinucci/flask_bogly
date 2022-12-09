"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Josh_Brolin_as_Thanos.jpeg/220px-Josh_Brolin_as_Thanos.jpeg"

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """model for Users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                           nullable=True)
    last_name = db.Column(db.String(15),
                          nullable=True)
    image_url = db.Column(db.Text, default = DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='author')

class Post(db.Model):
    """model for individual blog posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(70),
                      nullable=False,
                      unique=True)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.now())
    user_id = db.Column(db.Integer,
                           db.ForeignKey("users.id"))

class Tag(db.Model):
    """ Model for post tags """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                     unique=True)
    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

class PostTag(db.Model):
    """ Join model between Post and Tag models """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)