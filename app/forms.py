from flask.ext.wtf import FlaskForm
from wtforms import StringField, BooleanField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.validators import DataRequired, Optional
from .models import User, Goal
from app import app, db


class SignupForm(FlaskForm):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create Account")
 
  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not FlaskForm.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class LoginForm(FlaskForm):
    email = TextField('Email', [validators.Required('Please enter your email address'), validators.Email("Please enter your email address")])
    password = PasswordField('Password', [validators.Required('Please enter your password')])
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not FlaskForm.validate(self):
            return False
         
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False


class AnonForm(FlaskForm):
  submit = SubmitField('Try it Out in Anonymous Demo Mode!')

  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)

class AnonLogin(FlaskForm):
  anonIdLogin = TextField("Anonymous ID",  [validators.Required("Please Enter the Anonymous ID given during SignUp")])
  submit = SubmitField('Login with Anonymous ID')

  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)

  def validate(self):
    if not FlaskForm.validate(self):
      return False

    # anonUser = User.query.filter_by(firstname = 'anon').filter_by(lastname = self.anonIdLogin.data).first()
    anonUser = User.query.filter_by(firstname = 'anon').filter_by(lastname = self.anonIdLogin.data).first()
    if anonUser:
      return True
    else:
      self.anonIdLogin.errors.append('Invalid Anonymous Login ID')
      return False


class GoalForm(FlaskForm):
  title = StringField('Enter Goal', validators = [DataRequired()])
  description = StringField('Enter a Short Description', validators = [Optional()])
  youtubeURL = StringField('Search or Enter a Youtube Link', validators = [Optional()])

  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)





