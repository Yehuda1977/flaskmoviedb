import flask
import flask_sqlalchemy
import flask_migrate
import flask_login

app = flask.Flask(__name__)

# In case you have: "A secret key is required to use..."
app.config["SECRET_KEY"] = "my-very-secret-key"

# Format of a postgresSQL database url:
# postgresql://<username>:<password>@<hostname>:<port>/<db_name>


# WORKAROUND FOR DB ISSUES:
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/pynews"
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')
# END OF WORKAROUND

db = flask_sqlalchemy.SQLAlchemy(app)    # database bridge
migrate = flask_migrate.Migrate(app, db) # Migrator
login_manager = flask_login.LoginManager(app)

from . import routes, models

from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '9f48abce2dfcb47468c659a152b248a4'
tmdb.language = 'en'
tmdb.debug = True

