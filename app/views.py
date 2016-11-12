from flask import render_template, flash, redirect, request, session, url_for
from app import app, db
from .forms import LoginForm, SignupForm, AnonForm, AnonLogin
from .models import User#, AnonUser
from werkzeug import generate_password_hash
# from sqlalchemy import func

# @app.before_request
# def before_request():
#     if 'email' in session:
#         g.user = User.query.filter_by(email = session['email']).first()

"""Profile and App Handling"""

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))
    elif session['email'] == 'anon':
        # user = AnonUser.query.filter_by(anonid = session['anon']).first()
        user = User.query.filter_by(firstname = 'anon').filter_by(lastname = session['anon']).first()
    else:
        user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html', user = user, title='Home')


""" Regular Sign up and Login Routing"""
@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Kireet'} #fake user
    return render_template('index.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session: #check login
        return redirect(url_for('profile'))

    form = SignupForm()
    anonForm = AnonForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form, anonForm=anonForm)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email.lower() #store current session for login
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form, anonForm=anonForm)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('profile'))

    form = LoginForm()
    anonForm = AnonLogin()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, anonLoginForm = anonForm)
        else:
            session['email'] = form.email.data.lower()
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('login.html', form = form, anonLoginForm = anonForm)

"""Anonymous Sign Up and Login Routing"""


@app.route('/anonSignup', methods = ['GET', 'POST'])
def anonSignup():
    if request.method == 'GET':
        if 'email' in session:
            return redirect(url_for('profile'))

    if request.method == 'POST': #Must generate a limit based on request location (check if request is unique)
        
        # count = session.query(func.count(AnonUser.id)).scalar()
        count = User.query.filter_by(firstname = 'anon').count() #TODO:// Speed Up Count()
        anonId = generate_password_hash(str(count))

        currAnonUser = User.query.filter_by(firstname = 'anon').filter_by(lastname = anonId).first()

        if currAnonUser is None:
            anonUser = User('anon', anonId, anonId + '@gmail.com', str(count))
            db.session.add(anonUser)
            db.session.commit()

        session['email'] = 'anon'
        session['anon'] = anonId

        return redirect(url_for('profile'))

@app.route('/anonLogin', methods=['GET', 'POST'])
def anonLogin():
    if 'email' in session:
        return redirect(url_for('profile'))

    formLogin = LoginForm()
    anonLoginForm = AnonLogin()

    if request.method == 'POST': #Must generate a limit based on request location (check if request is unique)
        
        if not anonLoginForm.validate():
            return render_template('login.html', form = formLogin, anonLoginForm = anonLoginForm)
        else:
            # currAnonUser = AnonUser.query.filter_by(anonid = anonLoginForm.anonIdLogin.data).first()
            currAnonUser = User.query.filter_by(firstname = 'anon').filter_by(lastname = anonLoginForm.anonIdLogin.data).first()
            if currAnonUser is not None:
                session['email'] = 'anon'
                session['anon'] = anonLoginForm.anonIdLogin.data

            return redirect(url_for('profile'))

"""Logout Routing"""

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for Username="%s", remember_me=%s' %
#             (form.username.data, str(form.remember_me.data)))
#         return redirect('/index')

#     return render_template('login.html', title='Sign In', form=form )








