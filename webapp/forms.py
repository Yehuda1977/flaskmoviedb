import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

import wtforms
from wtforms import validators as vld
from .models import User

# Form class --> flask_wtf.FlaskForm
# Form fields --> wtforms.SomethingField

# each form is a class inheriting from flask_wtf.FlaskForm
# every class attribute is a field in the form

class QueryForm(flask_wtf.FlaskForm):
    
    query = wtforms.StringField("Query: ", validators=[vld.DataRequired(message="Input something..")])
    submit = wtforms.SubmitField("Search")

class CommentForm(flask_wtf.FlaskForm):

    comment = wtforms.StringField("Comment: ", validators=[vld.DataRequired(message="Make a comment..")])
    submit = wtforms.SubmitField("Submit Comment")




class SignUpForm(flask_wtf.FlaskForm):
    username = wtforms.StringField("Username: ", validators=[vld.DataRequired(message="This field cannot be empty.")])
    password = wtforms.PasswordField("Password: ", validators=[vld.Length(4, 12), vld.DataRequired(message="This field cannot be empty.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = wtforms.SubmitField("Sign up")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    def validate_field(self, field):
        user = User.query.filter_by(name=username.data).first()
        if user:
            raise vld.ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class SignInForm(flask_wtf.FlaskForm):
    username = wtforms.StringField("Username: ")
    password = wtforms.PasswordField("Password: ", validators=[vld.Length(4, 12)])

    submit = wtforms.SubmitField("Sign in")

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.name:
            user = User.query.filter_by(name=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


