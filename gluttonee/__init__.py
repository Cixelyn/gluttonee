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
from hyperpublic import Hyperpublic
from models import CreditCard
from models import User
from flaskext.mongokit import MongoKit

app = Flask(__name__)
app.debug = True
app.secret_key = 'omnomnom'

db = MongoKit(app)
db.register([CreditCard, User])

HYPERPUBLIC_KEY = 'eDuglow1SWQZjKFm58yUD2ZwBb2Tqfdem8ZgDnQP'
HYPERPUBLIC_SECRET = 'iouuCxwLmjSFgDCwlG0nQW5XwqHMSnbRQw7X54zT'
ORDRIN_API_KEY = 'pni78Hs4BGdV-pFu8bTaA'

hp_client = Hyperpublic(HYPERPUBLIC_KEY, HYPERPUBLIC_SECRET)

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
  if g.logged_in_user is not None:
    return 'You\'re already logged in.'
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
    newUser.state = request.form.get('state')
    newUser.zip = request.form.get('zip')
    newUser.phone = request.form.get('phone')
    newUser.credit_cards = []
    newUser.save()
    # log them in
    session['logged_in_id'] = newUser._id
    return 'New user %s created.' % newUser.email

@app.route('/new_credit_card', methods=['GET', 'POST'])
def new_credit_card():
  if g.logged_in_user is None:
    return 'You must be logged in to add a credit card.'
  if request.method == 'GET':
    return render_template('new_credit_card.html')
  if request.method == 'POST':
    newCard = db.CreditCard()
    newCard.number = request.form.get('number')
    newCard.code = request.form.get('code')
    newCard.exp_month = request.form.get('exp_month')
    newCard.exp_year = request.form.get('exp_year')
    newCard.first_name = request.form.get('first_name')
    newCard.last_name = request.form.get('last_name')
    newCard.street = request.form.get('street')
    newCard.city = request.form.get('city')
    newCard.zip = request.form.get('zip')
    newCard.state = request.form.get('state')
    newCard.save()
    g.logged_in_user.credit_cards.append(newCard)
    g.logged_in_user.save()
    return 'New credit card %s created for user %s.' % (
        newCard.number, g.logged_in_user.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if g.logged_in_user is not None:
    return 'You\'re already logged in.'
  if request.method == 'GET':
    return render_template('login.html')
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.User.find_one({'email':email, 'password':password})
    if user == None:
      return 'No such user.'
    session['logged_in_id'] = user._id
    return 'Sup %s %s!' % (user.first_name, user.last_name)

@app.route('/logout', methods=['GET'])
def logout():
  if g.logged_in_user is None:
    return 'You aren\'t logged in.'
  else:
    name = '%s %s' % (g.logged_in_user.first_name,
        g.logged_in_user.last_name)
    session.pop('logged_in_id', None)
    return 'Bye %s!' % name

@app.route('/get_delivering_restaurants', methods=['GET', 'POST'])
def get_delivering_restaurants():
  if g.logged_in_user is None:
    return 'You must be logged in to get a list of delivering restaurants.'
  if request.method == 'GET':
    return render_template('get_delivering_restaurants.html')
  if request.method == 'POST':
    Ordrin.api.initialize(ORDRIN_API_KEY, 'https://r-test.ordr.in')
    address = Ordrin.Address(
        g.logged_in_user.street,
        g.logged_in_user.city,
        g.logged_in_user.zip)
    datetime = Ordrin.dTime.now()
    datetime.asap()
    rawList = Ordrin.r.deliveryList(datetime, address)
    restaurants = json.loads(rawList)
    return rawList

@app.route('/get_ordrin_data', methods=['GET', 'POST'])
def get_ordrin_data():
  if g.logged_in_user is None:
    return 'You must be logged in to get Ordr.in data.'
  if request.method == 'GET':
    return render_template('get_ordrin_data.html')
  if request.method == 'POST':
    Ordrin.api.initialize(ORDRIN_API_KEY, 'https://r-test.ordr.in')
    rID = request.form.get('rID')
    restaurant = Ordrin.r.details(rID)
    return str(restaurant)

@app.route('/get_hyperpublic_data', methods=['GET', 'POST'])
def get_hyperpublic_data():
  if g.logged_in_user is None:
    return 'You must be logged in to get Hyperpublic data.'
  if request.method == 'GET':
    return render_template('get_hyperpublic_data.html')
  if request.method == 'POST':
    restaurant_name = request.form.get('restaurant_name')
    restaurant = None
    try:
      restaurant = hp_client.places.find(q=restaurant_name)[0]
    except:
      pass
    return str(restaurant)

@app.route('/order_from_restaurant', methods=['GET', 'POST'])
def order_from_restaurant():
  if g.logged_in_user is None:
    return 'You must be logged in to order from restaurants.'
  if len(g.logged_in_user.credit_cards) < 1:
    return 'You must have a credit card on file to order from restaurants.'
  if request.method == 'GET':
    return render_template('order_from_restaurant.html')
  if request.method == 'POST':
    Ordrin.api.initialize(ORDRIN_API_KEY, 'https://o-test.ordr.in')
    rID = request.form.get('rID')
    tray = request.form.get('tray')
    tip = request.form.get('tip')
    cc_index = int(request.form.get('cc_index'))
    credit_card = g.logged_in_user.credit_cards[cc_index]
    when = Ordrin.dTime.now()
    when.asap()
    first_name = g.logged_in_user.first_name
    last_name = g.logged_in_user.last_name
    delivery_address = Ordrin.Address(
        g.logged_in_user.street,
        g.logged_in_user.city,
        g.logged_in_user.zip)
    billing_address = Ordrin.Address(
        credit_card['street'],
        credit_card['city'],
        credit_card['zip'])
    orderResponse = Ordrin.o.submit(rID, tray, tip, when, first_name,
        last_name, delivery_address, credit_card['first_name'] + ' ' +
        credit_card['last_name'], credit_card['number'], credit_card['code'],
        credit_card['exp_month'] + '-' + credit_card['exp_year'], billing_address)
    return str(orderResponse)

@app.route('/drop', methods=['GET'])
def drop():
  # logout
  session.pop('logged_in_id', None)
  # TODO(jven): REMOVE THIS!!
  db.users.drop()
  return 'Robert\');--DROP TABLE students;--'

if __name__ == '__main__':
  app.run(debug=True)
