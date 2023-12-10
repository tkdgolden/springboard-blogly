from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """ Tests for model for Users. """

    def setUp(self):
        """ Clean up any existing users. """

        User.query.delete()

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_full_name(self):
        """ Test user init """

        first_name = "Alan"
        last_name = "Alda"
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Alan_Alda_2015.jpg/330px-Alan_Alda_2015.jpg"

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)

        self.assertEquals(user.full_name(), f"{first_name} {last_name}")