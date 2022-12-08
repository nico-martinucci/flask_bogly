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