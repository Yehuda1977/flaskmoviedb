import flask, flask_login
from flask import url_for
import requests

from . import app, db, fetch_movies       # . is webapp/
from . import forms, models
from tmdbv3api import Movie

movie = Movie()

@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/movies/query/<query>/<page>")
def query_movies(query, page):
    movies = fetch_movies.get_movies(query, page)
    return flask.render_template("movies.html", movies=movies, page=int(page), query=query)

@app.route("/movie/<int:id>", methods=["GET", "POST"])
def movie_details(id):
    m = movie.details(id)
    

    return flask.render_template("movie.html", movie=m)
    



@app.route("/movie-search", methods=["GET", "POST"])
def movie_search():
    form = forms.QueryForm()

    # case 1: Post request --> The user is sending data
    if flask.request.method == "POST":
        if form.validate_on_submit(): # Check all the validators
            url = flask.url_for("query_movies", query=form.query.data, page=1)
            # url --> /article/query/rick
            return flask.redirect(url)


    # case 2: Get request --> the user just wants to see the page
    return flask.render_template("movie_search.html", form=form)

    
    # return flask.redirect(url_for("signup"))

## Create a route:
# Form with one single field "query"
# Use the form data to display some articles about the query

# 1) Create the form        v
# 2) Create the route
# 3) Create the template that displays the form
# 4) Create the template that displays the articles

@app.route("/sign-up", methods=["GET","POST"])
def signup():
    """
    The function needs to add the user to the DB
    :return:
    """
    form = forms.SignUpForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Create user
            user = models.User(name=username, password=password)
            # Add it to the DB
            db.session.add(user)
            # Commit your changes
            db.session.commit()
            print(f"{username} was registered successfully")
            flask_login.login_user(user)
            flask.flash("User logged in successfully !", "success")

    return flask.render_template("signup.html", form=form)

@app.route("/sign-in", methods=["GET", "POST"])
def signin():
    form = forms.SignInForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Retrieve the user that matches this username
            user = models.User.query.filter_by(name=username).first()

            # Check the provided password against the user's one
            if user is not None and user.password == password:
                flask_login.login_user(user)
                flask.flash("User logged in successfully !", "success")
            else:
                flask.flash("Something went wrong.", "danger") # Put the message into the flashed messages
                # To retrieve those messages: flask.get_flashed_messages()

    return flask.render_template("signin.html", form=form)

@app.route("/sign-out")
def signout():
    flask_login.logout_user()
    return flask.redirect('/')


# Create a route that displays a list of all the registered users
@app.route("/users")
def users_list():
    # Retrieve users
    users = models.User.query.all()            # Return a list of users
    # users = [<User 1>, <User 2>]
    # my_user = users[0]
    # print(my_user.name)
    # print(my_user.password)


    # Create users_list.html
    return flask.render_template("users_list.html", users=users)


# Route: profile page
@app.route('/user/<int:user_id>')
def profile_page(user_id):

    # Query methods:
    # Class.query.all() --> Returns a list of all the objects
    # Class.query.filter_by(attr=value) --> Return a list of all the objects that match the condition
    # Class.query.get(primary_key) --> Retrieve an object by its PK

    # Retrieve the user
    user = models.User.query.get(user_id)

    return flask.render_template("user_profile.html", user=user)


# Step 1: Displaying the favourite quote on the user page
# Step 2: (Because quote<->user is a one to one, one quote can be linked to only one user)
#       --> In quotes_list, display only the quotes that aren't the fav quote of a user
# Step 3: Creating a route fav_quote(quote_id) --> Sets the quote as the fav quote of the logged in
#        user
# Step 4: In the quotes_list: Add a button next to each quote (if the user is authenticated) to make
#        the quote his fav quote



@app.route("/add-movie/<int:id>", methods=["GET","POST"])
def add_movie(id):
    # return "Protected"
    
    m = movie.details(id)
    
    try:
        movie_obj = models.Movie(title=m.title, description=m.overview, poster_path=m.poster_path, movie_id=m.id)
        db.session.add(movie_obj)
    except:
        pass

    db.session.commit()

    if flask_login.current_user.is_authenticated: # The user is logged in
        if movie_obj not in flask_login.current_user.fav_movies:
            flask_login.current_user.fav_movies.append(movie_obj) # fav_books is a list of <Book> objects
            db.session.commit()

    else:
        flask.flash("You need to be logged in")
        

    return flask.redirect("/sign-in")

@app.route("/movie/<int:movie_id>/comment/<int:comment_id>", methods=["GET", "POST"])
def movie_comment(movie_id, comment_id):
    pass

@app.route("/delete/<int:id>")
def delete_fav(id):
    pass








