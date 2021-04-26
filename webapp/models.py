# MODELS.py
import flask_login

from . import db, login_manager  # Database bridge created in __init__.py

# First step:
# Secondary table for the User<>Book ManyToMany relationship
user2movies = db.Table(
    "user2movies", # name of the table
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer(), db.ForeignKey("movie.id"), primary_key=True),
) # PK will be a combination of the two (1-2)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, flask_login.UserMixin): # db.Model is required if you want to create an SQL model
    """
    user
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    |  id (PK)  |  name (str64)  |  password (str64)  |  fav_quote (int) --> FK to Quote   | fav_quote_id (BTS) |
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    |           |                |                    |          <Quote> object            |        1           |
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    """
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64))

    # Step 2: relationship
    fav_movies = db.relationship("Movie", backref="users", secondary=user2movies)


class Movie(db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(64))
    poster_path = db.Column(db.String(128))
    description = db.Column(db.String(64))
    movie_id = db.Column(db.Integer())
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # author_id = db.Column(db.Integer(), db.ForeignKey("human.id"))

