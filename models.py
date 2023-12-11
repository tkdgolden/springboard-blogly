"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ A User has id, first name, last name, and profile image url. """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable = False)
    image_url = db.Column(db.String)
    posts = db.relationship('Post')

    def __repr__(self):
        """ Show info about user. """

        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"


    def full_name(self):
        """ Full name """

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """ A Post has id, title, content, datetime, and user which connects to User. """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(100),
                      nullable = False)
    content = db.Column(db.String,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')

