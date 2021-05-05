# MODELS.py
import flask_login
from datetime import datetime

from . import db, login_manager  # Database bridge created in __init__.py

# First step:
# Secondary table for the User<>Book ManyToMany relationship
user2movies = db.Table(
    "user2movies", # name of the table
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer(), db.ForeignKey("movie.id"), primary_key=True),
) # PK will be a combination of the two (1-2)

movie2comments = db.Table(
    "movie2comments", # name of the table
    db.Column("comment_id", db.Integer(), db.ForeignKey("comment.id"), primary_key=True),
    db.Column("movie_id", db.Integer(), db.ForeignKey("movie.id"), primary_key=True),
) # PK will be a combination of the two (1-2)

# user2comments = db.Table(
#     "user2comments", # name of the table
#     db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
#     db.Column("comment_id", db.Integer(), db.ForeignKey("comment.id"), primary_key=True),
# )

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, flask_login.UserMixin): # db.Model is required if you want to create an SQL model
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpeg')
    # Step 2: relationship
    fav_movies = db.relationship("Movie", backref="users", secondary=user2movies)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    poster_path = db.Column(db.String(128))
    description = db.Column(db.String(64))
    movie_id = db.Column(db.Integer(), unique=True, nullable=False)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    movie_comments = db.relationship("Comment", backref="comments", secondary=movie2comments)

    

class Comment(db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.String(280), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    


    def __repr__(self):
        return f"Post('{self.author_id}', '{self.date_posted}')"

    