"""
Gluttonee web application.
"""

__author__ = 'Cory Li (coryli@mit.edu), Justin Venezuela (jven@mit.edu)'

import json
import Ordrin
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import session
from flask import render_template
from foursquare import FoursquareAuthHelper
from foursquare import FoursquareClient
from models import User
from flaskext.mongokit import MongoKit

app = Flask(__name__)
app.debug = True
app.secret_key = 'omnomnom'

db = MongoKit(app)
db.register([User])

FOURSQUARE_KEY = 'YKM4DZK0JBRA1UY4QWR0TJHCB5HUM2423RVXLNSRKGKV5YWA'
FOURSQUARE_SECRET = '3UN4F2Z1ROFXY21CLVMSWCTEBL5EJOPAMMFATKCWXXQP15YL'
ORDRIN_API_KEY = 'pni78Hs4BGdV-pFu8bTaA'

fs_auth = FoursquareAuthHelper(FOURSQUARE_KEY, FOURSQUARE_SECRET, 'http://hacknyc.org')
fs_access_token = fs_auth.get_access_token('200')
fs_client = FoursquareClient(fs_access_token)

@app.before_request
def before_request():
  if 'logged_in_id' in session:
    g.logged_in_user = db.User.find_one(session['logged_in_id'])
  else:
    g.logged_in_user = None

@app.route('/', methods=['GET'])
def home():
  return render_template('home.html')

@app.route('/home', methods=['GET'])
def home_test():
  if g.logged_in_user is not None:
    return 'You\'re logged in as %s.' % g.logged_in_user.email
  else:
    return 'You\'re not logged in.'

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  if request.method == 'POST':
    # make sure user with this email doesnt exist
    user = db.User.find_one({'email':request.form.get('email')})
    if user is not None:
      return 'A user with this e-mail already exists.'
    # make new user
    newUser = db.User()
    newUser.first_name = request.form.get('first_name')
    newUser.last_name = request.form.get('last_name')
    newUser.email = request.form.get('email')
    # TODO(jven): hash this shit
    newUser.password = request.form.get('password')
    newUser.street = request.form.get('street')
    newUser.city = request.form.get('city')
    newUser.zip = request.form.get('zip')
    newUser.state = request.form.get('state')
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

@app.route('/get_restaurants', methods=['GET', 'POST'])
def get_restaurants():
  if g.logged_in_user is None:
    return 'You must be logged in to get a list of restaurants.'
  if request.method == 'GET':
    return render_template('get_restaurants.html')
  if request.method == 'POST':
    Ordrin.api.initialize(ORDRIN_API_KEY, 'https://r-test.ordr.in')
    place = Ordrin.Address(
        g.logged_in_user.street,
        g.logged_in_user.city,
        g.logged_in_user.zip,
        u'',
        g.logged_in_user.state,
        g.logged_in_user.phone,
        'my_location')
    when = Ordrin.dTime.now()
    when.asap()
    rawList = Ordrin.r.deliveryList(when, place)
    restaurants = json.loads(rawList)
    return str(restaurants)

@app.route('/get_foursquare_ratings', methods=['GET', 'POST'])
def get_foursquare_ratings():
  if g.logged_in_user is None:
    return 'You must be logged in to get Foursquare ratings.'
  if request.method == 'GET':
    return render_template('get_foursquare_ratings.html')
  if request.method == 'POST':
    Ordrin.api.initialize(ORDRIN_API_KEY, 'https://r-test.ordr.in')
    place = Ordrin.Address(
        g.logged_in_user.street,
        g.logged_in_user.city,
        g.logged_in_user.zip,
        u'',
        g.logged_in_user.state,
        g.logged_in_user.phone,
        'my_location')
    when = Ordrin.dTime.now()
    when.asap()
    rawList = Ordrin.r.deliveryList(when, place)
    restaurants = json.loads(rawList)
    restaurant_names = [restaurant['na'] for restaurant in restaurants]
    fs_ratings = [fs_client.make_api_call(
        fs_client.API_URL + '/venues/search',
        method='GET',
        query={'name':restaurant_name}) for restaurant_name in restaurant_names]
    return str(fs_ratings)

@app.route('/drop', methods=['GET'])
def drop():
  # logout
  session.pop('logged_in_id', None)
  # TODO(jven): REMOVE THIS!!
  db.users.drop()
  return 'Robert\');--DROP TABLE students;--'

if __name__ == '__main__':
  app.run(debug=True)
