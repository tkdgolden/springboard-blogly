from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ Tests for views for Users. """

    def setUp(self):
        """ Add sample user. """
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Alan", last_name="Alda", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Alan_Alda_2015.jpg/330px-Alan_Alda_2015.jpg")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()

    def test_list_users(self):
        """ Test display of all users list. """

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)

    def test_new_form(self):
        """ Test display of blank new user form """

        with app.test_client() as client:
            resp = client.get(f"/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Provide', html)

    def test_submit_new(self):
        """ Test submission of new user """

        with app.test_client() as client:
            d = {"fname": "Gary", "lname": "Burghoff", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/GaryBurghoff03.jpg/330px-GaryBurghoff03.jpg"}
            resp = client.post('/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Gary Burghoff</h1>', html)
            self.assertIn("Burghoff", html)

    def test_detail(self):
        """ Test user detail page """

        with app.test_client() as client:
            resp = client.get(f"/user/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button type="button">Back to All Users</button>', html)

    def test_edit_form(self):
        """ Test edit user form """

        with app.test_client() as client:
            resp = client.get(f"/edit/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a User</h1>', html)
            self.assertIn('value="Alan"', html)

    def test_submit_edit(self):
        """ Test submission of edit user form """

        with app.test_client() as client:
            d = {"fname": "Gary", "lname": "Burghoff", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/GaryBurghoff03.jpg/330px-GaryBurghoff03.jpg"}
            resp = client.post('/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Gary Burghoff</h1>', html)
            self.assertIn("Burghoff", html)

class PostViewsTestCase(TestCase):
    """ Tests for views for Posts. """

    def setUp(self):
        """ Add sample post. """
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Alan", last_name="Alda", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Alan_Alda_2015.jpg/330px-Alan_Alda_2015.jpg")

        db.session.add(user)
        db.session.commit()

        Post.query.delete()

        post = Post(title="Wounds", content="Look Colonel, I'll heal their wounds, treat their wounds, bind their wounds, but I will not inflict their wounds.", user_id=user.id)

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()

    def test_user_posts(self):
        """ Tests posts show on user detail page. """

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('wounds', html)

    def test_post_form(self):
        """ Test display of blank add post form """

        with app.test_client() as client:
            resp = client.get(f"/add/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('for Alan Alda', html)

    def test_submit_post(self):
        """ Test submission of new user """

        with app.test_client() as client:
            d = {"title": "Hell", "content": "War isn't Hell. War is war, and Hell is Hell.  And of the two, war is a lot worse.", "user_id": {self.user_id}}
            resp = client.post(f'/add/{self.user_id}', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Hell</h1>', html)

    def test_post_detail(self):
        """ Tests post page """

        with app.test_client() as client:
            resp = client.get(f"/post/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('wounds', html)

    def test_change_post_form(self):
        """ Tests edit form page """

        with app.test_client() as client:
            resp = client.get(f"/change/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)
            self.assertIn('value="Wounds"', html)

    def test_submit_post_change(self):
        """ Tests submission of edit post form """

        with app.test_client() as client:
            d = {"title": "Hell", "content": "War isn't Hell. War is war, and Hell is Hell.  And of the two, war is a lot worse.", "user_id": {self.user_id}}
            resp = client.post(f"/change/{self.post_id}", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Hell</h1>', html)

