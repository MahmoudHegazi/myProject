from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from database_setup1 import Base, newUrls, Skills, Users
from flask import session as login_session
import random
from datetime import datetime
from datetime import date
import string
# IMPORTS FOR THIS STEP
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///mpasta.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def makeurl():
    mynames = ['dragons boy', 'man boys', 'ninja drakess']
    words = ['dragon', 'boy', 'man', 'girl', 'ninja',
             'fighter', 'hell', 'drake', 'master', 'nightfal',
             'harder', 'forbedin', 'f', 'g', 'b', 'cc', 'customer',
             'line', 'svg', 'snake', 'python', 'coder', 'developer',
             'htmls', 'websites', 'servers', 'myservers', 'myserversn',
             'takeservers', 'theservers', 'aservers', 'myserversm',
             'killer', 'montroh', 'hypergens', 'kongfu', 'kontio',
             'myrekon', 'mostrs', 'hpyerkz', 'funkyrock', 'lopto',
             'mahmoud', 'ahmed', 'mohamed', 'keygen', 'super',
             'farmer', 'draven', 'lux', 'daruis', 'zed', 'night',
             'helor', 'kofono', 'hello', 'world']
    words1 = ['dragons', 'boys', 'mans', 'girls', 'ninjas',
             'fighters', 'hells', 'drakess', 'masters', 'nightfals',
             'harders', 'forbedins', 'n', 'c', 'd', 'bb', 'customers'
             'lines', 'sbg', 'snakes', 'pythons', 'coders', 'developers'
             'htmls', 'websites', 'servers', 'myservers', 'as',
              'sd', 'qw', 'er', 'hello', 'get', 'git', 'world', 'qwe',
              'big','host', 'hosters', 'hend', 'amira', 'may', 'mary',
              'kings', 'casser', 'ghj' , 'git']
    first = random.choice(words)
    second = random.choice(words1)
    exist = None
    newurl = None
    newurl = first + second
    exist = session.query(newUrls).filter_by(name=newurl).first()
    if newurl == exist:
        print('This Error taken before')
        exist = True
    else:
        exist = False
        
    return newurl
    
    




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    def age(birthdate):
	today = date.today()
	return today.year - birthdate.year - ((today.month,
				       today.day) < (birthdate.month,
						     birthdate.day))
    def salatMaker():
        letters = string.ascii_lowercase    
        return ''.join(random.choice(letters) for i in range(10))

                                 
    if request.method == 'POST':
        birthdate = request.form['birth']
        umain = request.form['psw']
        #use indexing if you know the key exists
        name = request.form['name']      
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        user_age = age(birthdate)
        user_salat = salatMaker()        
        user_idea = str(hash(umain + user_salat))[::-1]
        print(user_idea)
        newuser = Users(name="kosomk")
        session.add(newuser)
        session.commit()
        #return redirect(url_for('editor'))
    else:
        return render_template('signup.html')
        
    return "user with name %s Has Succesfully Created" %newuser.name
    
    
    
"""
        #newUser = Users(name=name, password=user_idea, gender=gender)
        #age=user_age, birthd = birthdate,job=job
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['umail']
        idea_user = request.form['psw']
        try:
            user = session.query(Users).filter_by(email=user_name).one()
        except:
            problem = "This User Not Registeried Yet"
            return render_template('login.html', problem = problem)
            
        if user:
            user_idea = str(hash(idea_user + user.salaty))[::-1]
            if user_idea == user.password:
                #looks like important but i forget why
                link = '/profile/' + str(user.id) + '/'
                flash('Nice to see you again Mr %s' % user.name)
                login_session['username'] = user.username
                login_session['id'] = user.id
                login_session['name'] = user.name
                login_session['gender'] = user.gender
                login_session['age'] = user.age
                login_session['birthdate'] = user.birthd
                login_session['email'] = user.email
                return redirect(url_for('editor'))
            else:
                flash('Sorry You have enter wrong pass or user Try Again')
                return render_template('login.html')
        else:
            problem = "Sorry You have enter wrong pass or user click forget password!"
            return render_template('login.html', problem = problem)
"""



@app.route('/logout', methods=['get'])
def disconnect():
    del login_session['mail']
    del login_session['name']
    del login_session['user_id']    
    response = make_response(json.dumps(
    'Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    flash('Successfully disconnected Bye Bye.')
    return redirect(url_for('editor'))  


@app.route('/')
@app.route('/editor', methods=['GET'])
def editor():
           
        if 'mail' not in login_session:
            return render_template('login.html')
            
        else:
            user = login_session['user_id']
            try:
                templates = session.query(newUrls).filter_by(user_id=user).all()
                if templates:
                    templates = templates
            except:
                templates = ['no Saved Templates']              
        return render_template('index.html', templates=templates)


@app.route('/compiler', methods=['GET', 'POST'])
def compiler():

    if request.method == 'POST':
    
        code=request.form.get('codes')
        user_url = makeurl() 
        output = ""
        output += code
        output += '<br /><br /><a href="/">Run another code</a>'
        output += '<br /><br /><p>Your Code Can be fonded here'
        output += ': <a href="http://127.0.0.1:5000/host/' + user_url + '">' + "/host/" + user_url + '</a>'
        fullurl = 'http://127.0.0.1:5000/host/%s' %user_url
        if output:
            newPage = newUrls(name=user_url, code=code, url=fullurl)
            session.add(newPage)        
        flash('Here are Your Link: %s' % newPage.url)
        session.commit()

        
        return output
        
    else:    
        return render_template('index.html')        
 

@app.route('/host/<string:user_url>/', methods=['GET'])
def getpage(user_url):    
    gettemplate = session.query(newUrls).filter_by(name=user_url).first()
    userpage = gettemplate.code
    return userpage





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
