"""
Gluttonee web application.
"""

__author__ = 'Cory Li (coryli@mit.edu), Justin Venezuela (jven@mit.edu)'

import Ordrin
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import session
from flask import render_template
from models import User
from flaskext.mongokit import MongoKit

app = Flask(__name__)
app.debug = True

db = MongoKit(app)
db.register([User])

@app.before_request
def before_request():
  if 'logged_in_id' in session:
    g.logged_in_user = db.User.find_one(session['logged_in_id'])
  else:
    g.logged_in_user = None

@app.route('/', methods=['GET'])
def home():
  # if g.logged_in_user is not None:
  #   return 'You\'re logged in as %s.' % g.logged_in_user.email
  # else:
  #   return 'You\'re not logged in.'
  return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  if request.method == 'POST':
    newUser = db.User()
    newUser.first_name = request.form.get('first_name')
    newUser.last_name = request.form.get('last_name')
    newUser.email = request.form.get('email')
    # TODO(jven): hash this shit
    newUser.password = request.form.get('password')
    newUser.address = request.form.get('address')
    newUser.credit_card_number = request.form.get('credit_card_number')
    newUser.credit_card_code = request.form.get('credit_card_code')
    newUser.credit_card_exp_month = request.form.get('credit_card_exp_month')
    newUser.credit_card_exp_year = request.form.get('credit_card_exp_year')
    newUser.save()
    return 'New user %s created.' % newUser.email

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  if request.method == 'POST':
    try:
      email = request.form.get('email')
      password = request.form.get('password')
    except:
      return 'Error trying to login.'
    user = db.User.find_one({'email':email, 'password':password})
    if user == None:
      return 'No such user.'
    session['logged_in_id'] = user._id
    return 'Sup %s %s!' % (user.first_name, user.last_name)

@app.route('/logout', methods=['GET'])
def logout():
  if g.logged_in_user is not None:
    name = '%s %s' % (g.logged_in_user.first_name,
        g.logged_in_user.last_name)
    session.pop('logged_in_id', None)
    return 'Bye %s!' % name
  else:
    return 'You weren\'t logged in.'

@app.route('/get_restaurants', methods=['POST'])
def get_restaurants():
  pass

if __name__ == '__main__':
  app.run(debug=True)
