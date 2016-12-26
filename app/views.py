from flask import render_template, flash, redirect, request, session, url_for, jsonify
from app import app, db
from .forms import LoginForm, SignupForm, AnonForm, AnonLogin, GoalForm
from .models import User, Goal
from .quoteManager import Forismatic
from werkzeug import generate_password_hash

from datetime import datetime
import urllib.request
import urllib.parse
import re

# @app.before_request
# def before_request():
#     if 'email' in session:
#         g.user = User.query.filter_by(email = session['email']).first()


def suggestVideo(title, description):
    """
    These will be the randomized client side-generated videos for users who have not entered
    a youtubeURL/search for a video. It will later be saved for future references.

    youtubeAPI search. integrate youtubeAPI with nltk package called on the title and description...
    Learn from the title and description and then offer new content ID to clientside JS to render.
    """
    
    query_string = urllib.parse.urlencode({"search_query" : input()})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("http://www.youtube.com/watch?v=" + search_results[0])
    return




f = Forismatic()

def getQuote():


def suggestQuote(title, description, count=0):
    """
    Using a quotes database, relationship between title, description : quote and author
    """
    quote = f.get_quote()
    if quote is not None:
        return q
    else:
        return suggestQuote(title, description, count += 1)

    # print(q.quote, q.author)
    # return 

def suggestMusic(title, description):
    """
    DFT on music, cluster into different groups with k-means
    OR
    Dataset of song with genre, then find a relationship with supervised title and description
    """
    return

def suggestImage(title, description):
    """
    Use OpenCV or Google Vision to match the title & description to first 10 returned items from a 
    google image search (Custom Google Search Engine) of the title

    OR against a db of stock images.
    """
    return



"""Profile and Current User Handling"""

def getCurrentUser():
    if 'email' not in session:
        return None

    elif session['email'] == 'anon':
        # user = AnonUser.query.filter_by(anonid = session['anon']).first()
        user = User.query.filter_by(firstname = 'anon').filter_by(lastname = session['anon']).first()
    else:
        user = User.query.filter_by(email = session['email']).first()

    return user

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    user = getCurrentUser()
    if user == None:
        return redirect(url_for('login'))

    if user is None:
        return redirect(url_for('login'))
    else:
        form = GoalForm()
        goals = user.getGoals()
        #AJAX on Client will call the suggestion code, which will return the random quote/image/music
        #from the suggestions above ^^.
        return render_template('profile.html', user = user, title='Home', form = form, goals = goals)



"""Server Side Goal Handling"""

@app.route('/updateGoalOrder', methods = ['POST'])
def updateGoalOrder():
    goalOrder = request.get_json(silent=True)['values']
    user = getCurrentUser()
    if user == None:
        return redirect(url_for('login'))

    for i in range(len(goalOrder)):
        goal = Goal.query.filter_by(user_id = user.id).filter_by(id = int(goalOrder[i])).first()
        goal.order = i
        db.session.commit()

    return jsonify({ 'response': 'success' })



@app.route('/createGoal', methods = ['GET','POST'])
def createGoal():
    user = getCurrentUser()
    if user == None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        form = GoalForm()
        if form.validate():
            #form.youtubeURL.data.split('v=')[-1]
            #"YinkbnaBgIk"
            #Process the string (either search YouTube and return first result or split and save)
            if 'www.youtube' in form.youtubeURL.data:
                youtube = str(form.youtubeURL.data.split('v=')[-1])
            else:
                # youtube = youtubeAPI for the first search result ID
                youtube = "YinkbnaBgIk"

            try: 
                prevGoal = Goal.query.filter_by(user_id = user.id).order_by(Goal.order.desc()).first().order
                prevGoal = prevGoal + 1
            except:
                prevGoal = 0

            goal = Goal(title = form.title.data, timestamp = datetime.utcnow(),
                user_id = user.id, description = form.description.data,
                youtubeURL = youtube, order = prevGoal)
            db.session.add(goal)
            db.session.commit()
            return redirect(url_for('profile'))

        flash('There was an error in your goal')

    return redirect(url_for('profile'))

@app.route('/editGoal/<int:id>', methods = ['GET','POST'])
def editGoal(id):
    user = getCurrentUser()
    if user == None:
        return redirect(url_for('login'))

    editableGoal = Goal.query.filter_by(id = id).first()

    if editableGoal != None:
        if editableGoal.user_id != user.id:
            flash('You cannot edit this post')
            redirect(url_for('profile'))
        else:
            goals = user.getGoals() #Should do something with this?
            form = GoalForm(obj = editableGoal)
            form.populate_obj(editableGoal)
            #Change to add Goal instead of in profile
            if request.method == 'POST':
                if form.validate():
                    editableGoal.title = form.title.data
                    editableGoal.description = form.description.data
                    # editableGoal.youtubeURL = form.youtubeURL.data
                    #Process the string (either search YouTube and reutnr first result or split and save)
                    editableGoal.youtubeURL = str(form.youtubeURL.data.split('v=')[-1])
                        
                    if 'www.youtube' in form.youtubeURL.data:
                        editableGoal.youtubeURL = str(form.youtubeURL.data.split('v=')[-1])
                    else:
                        # youtube = youtubeAPI for the first search result ID
                        editableGoal.youtubeURL = "YinkbnaBgIk"

                    db.session.commit()
                    return redirect(url_for('profile'))

        return render_template('editGoal.html', form = form, editableGoal = editableGoal)
        #return render_template('profile.html', user = user, title='Home', form = form, goals = goals, editableGoal = editableGoal)

    return redirect(url_for('profile'))

@app.route('/deleteGoal/<int:id>', methods = ['GET'])
def deleteGoal(id):
    user = getCurrentUser()
    if user == None:
        return redirect(url_for('login'))

    editableGoal = Goal.query.filter_by(id = id).first()

    if editableGoal != None:
        if editableGoal.user_id != user.id:
            flash('You cannot delete this goal')
        else:
            db.session.delete(editableGoal)
            db.session.commit()
    return redirect(url_for('profile'))


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
    session.pop('anon', None)
    return redirect(url_for('index'))




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for Username="%s", remember_me=%s' %
#             (form.username.data, str(form.remember_me.data)))
#         return redirect('/index')

#     return render_template('login.html', title='Sign In', form=form )








