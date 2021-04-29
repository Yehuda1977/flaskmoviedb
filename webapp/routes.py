import flask, flask_login
from flask import url_for
import requests

from . import app, db, fetch_movies      # . is webapp/

from . import forms, models
from tmdbv3api import Movie
from . import bcrypt

movie = Movie()

@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/movies/query/<query>/<page>")
def query_movies(query, page):
    movies = fetch_movies.get_movies(query, page)
    if movies['total_results'] == 0:
        flask.flash("There are no movies that contain that word.", "danger")
        return flask.redirect(url_for('movie_search'))
    else:
        return flask.render_template("movies.html", movies=movies, page=int(page), query=query)
        

@app.route("/movie/<int:id>", methods=["GET", "POST"])
def movie_details(id):
    # form = forms.CommentForm()
    
    m = movie.details(id)
    already_added = False
    #check that this movie hasn't been added before
    if flask_login.current_user.is_authenticated: # The user is logged in
        for mo in flask_login.current_user.fav_movies:
            if mo.movie_id == m.id:
                already_added = True
    
    # if flask.request.method == "POST":
    #     if form.validate_on_submit(): 
    #         comment = form.comment.data

    #         # Create user
    #         comm = models.Comment(comment=comment)
    #         # Add it to the DB
    #         db.session.add(comm)
    #         # Commit your changes
    #         db.session.commit()
    #         print(f"{comm} was added successfully")
            
    #         flask.flash("Comment added successfully !", "success")

                
    return flask.render_template("movie.html", movie=m, already_added=already_added)
    
    
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


@app.route("/add-movie/<int:id>", methods=["GET","POST"])
def add_movie(id):

    m = movie.details(id)
    if flask_login.current_user.is_authenticated:
        mo = models.Movie.query.filter_by(movie_id=id).first()
    #check that this movie hasn't been added before to the general movie db
    if flask_login.current_user.is_authenticated: # The user is logged in
        if mo:
            movie_obj = models.Movie.query.filter_by(movie_id=id).first()
        else:
            try:
                movie_obj = models.Movie(title=m.title, description=m.overview, poster_path=m.poster_path, movie_id=m.id)
                db.session.add(movie_obj)
            except:
                pass

    db.session.commit()

    if flask_login.current_user.is_authenticated: # The user is logged in
        if movie_obj not in flask_login.current_user.fav_movies:
            flask_login.current_user.fav_movies.append(movie_obj) # fav_movies is a list of <Book> objects
            db.session.commit()

    else:
        flask.flash("You need to be logged in")
        

    # return flask.redirect("/sign-in")
    if flask_login.current_user.is_authenticated:
        return flask.render_template("user_profile.html", user=flask_login.current_user)
    



@app.route("/getmoviesindb")
def getmovies():
    all_movies = models.Movie.query.all()

    if all_movies:
        # Create users_list.html
        return flask.render_template("movies_in_db.html", movies=all_movies)
    else:
        flask.flash("No movies have been added to the database.", "danger")
        return flask.redirect('/')


@app.route("/delete/<int:id>")
def delete_fav(id):
    pass


@app.route("/movie/<int:movie_id>/comment", methods=["GET", "POST"])
def movie_comment(movie_id):
    form = forms.CommentForm()


    if flask_login.current_user.is_authenticated: # The user is logged in
        mo = models.Movie.query.filter_by(movie_id=movie_id).first()

        if mo:
            if flask.request.method == "POST":
                if form.validate_on_submit(): 
                    if form.validate_on_submit():
                        comment = form.comment.data

                        # Create comment
                        comm = models.Comment(content=comment)
                        # Add it to the DB
                        db.session.add(comm)
                        # Commit your changes
                        
                        print(f"{comm} was added successfully")
                        mo.movie_comments.append(comm)

                        db.session.commit()
                        flask.flash("Comment added successfully !", "success")

                    
    return flask.render_template("addcomment.html", form=form)
    





###########################################################
###########################################################
###########################################################
###########################################################
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
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            user = models.User.query.filter_by(name=username).first()

            if not user:
            # Create user
                user = models.User(name=username, password=hashed_password)
                # Add it to the DB
                db.session.add(user)
                # Commit your changes
                db.session.commit()
                print(f"{username} was registered successfully")
                flask_login.login_user(user)
                flask.flash("User logged in successfully !", "success")
            else:
                flask.flash("User with that name already exists. Please try again.", "danger")

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
            if user and bcrypt.check_password_hash(user.password, password):
                flask_login.login_user(user)
                flask.flash("User logged in successfully !", "success")
                return flask.render_template('user_profile.html', user=user)
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

    if users:
    # Create users_list.html
        return flask.render_template("users_list.html", users=users)
    else:
        flask.flash("No users have been added to the database.", "danger")
        return flask.redirect('/')


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






