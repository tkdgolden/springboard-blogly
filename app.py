"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag
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
    posts = Post.query.order_by(Post.created_at).limit(5)
    tags = Tag.query.all()
    return render_template("list.html", users=users, posts=posts, tags=tags)

@app.route("/new", methods=["GET", "POST"])
def add_user():
    """ Add new user and redirect to their details """

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

        return redirect(f"/user/{user.id}")

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    """ Show info on a single user. """

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("detail.html", user=user, posts=posts)

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

        return redirect(f"/user/{user.id}")
    
@app.route("/delete/user/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    """ Deletes a single user and returns to list page """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route("/post/<int:post_id>")
def post(post_id):
    """ Displays a single post content """

    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', post=post)

@app.route("/add/<int:user_id>", methods=["GET", "POST"])
def add_post(user_id):
    """ Adds a new post and redirects to post page """

    user = User.query.get_or_404(user_id)

    if request.method == "GET":
        tags = Tag.query.all()

        return render_template("add.html", user=user, tags=tags)
    
    elif request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tags')
        tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get_or_404(tag_id)
            tags.append(tag)
        post = Post(title=title, content=content, user_id=user.id, tags=tags)


        db.session.add(post)
        db.session.commit()

        return redirect(f"/post/{post.id}")
    
@app.route("/change/<int:post_id>", methods=["GET", "POST"])
def change_post(post_id):
    """ Changes a post and redirects to post page """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == "GET":
        return render_template("change.html", post=post, tags=tags)
    
    elif request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        db.session.commit()

        return redirect(f"/post/{post.id}")
    
@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    """ Delete a post from database, return to user """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/user/{post.user_id}")

@app.route("/tag/<int:tag_id>")
def tag_posts(tag_id):
    """ Show all posts with a given tag """

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag.html", tag=tag)

@app.route("/create", methods=["GET", "POST"])
def create_tag():
    """ Create a tag and return to list page """

    if request.method == "GET":
        return render_template("create.html")

    elif request.method == "POST":
        name = request.form['name']

        tag = Tag(name=name)

        db.session.add(tag)
        db.session.commit()

        return redirect("/")
    
@app.route("/delete/tag/<int:tag_id>")
def delete_tag(tag_id):
    """ Delete a tag and return to list page """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/")

@app.route("/modify/<int:tag_id>", methods=["GET", "POST"])
def modify_tag(tag_id):
    """ Modify a tag name and return to tag page """

    tag = Tag.query.get_or_404(tag_id)

    if request.method == "GET":
        return render_template("modify.html", tag=tag)
    
    elif request.method == "POST":
        name = request.form['name']

        tag.name = name

        db.session.commit()

        return redirect(f"/tag/{tag_id}")