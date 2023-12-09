"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ A User has id, first name, last name, and profile image url. """

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable = False)
    image_url = db.Column(db.String(100))

    def full_name(self):
        """ Full name """

        return f"{self.first_name} {self.last_name}"

