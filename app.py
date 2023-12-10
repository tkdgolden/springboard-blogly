"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET"

debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

default_image = "https://picsum.photos/536/354"

@app.route("/")
def list_users():
    """ List users and show add form. """

    users = User.query.order_by(User.last_name).order_by(User.first_name).all()
    return render_template("list.html", users=users)

@app.route("/new", methods=["GET", "POST"])
def add_user():
    """ Add new user and redirect to list """

    if request.method == "GET":
        return render_template("new.html")

    elif request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        if (request.form['image']):
            image_url = request.form['image']
        else:
            image_url = default_image
        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()

        return redirect(f"/{user.id}")

@app.route("/<int:user_id>")
def user_detail(user_id):
    """ Show info on a single user. """

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    """ Edit a single user and return to user info """

    user = User.query.get_or_404(user_id)

    if request.method == "GET":
        return render_template("edit.html", user=user)
    
    elif request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        image_url = request.form['image']

        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.commit()

        return redirect(f"/{user.id}")
    
@app.route("/delete/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    """ Deletes a single user and returns to list page """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')