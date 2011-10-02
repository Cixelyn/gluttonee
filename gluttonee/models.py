"""
MongoDB document models.
"""

__author__ = 'Cory Li (coryli@mit.edu), Justin Venezuela (jven@mit.edu)'

from flaskext.mongokit import Document

class User(Document):
  __collection__ = 'users'
  structure = {
      'first_name':unicode,
      'last_name':unicode,
      'email':unicode,
      'password':unicode,
      'street':unicode,
      'city':unicode,
      'state':unicode,
      'zip':unicode,
      'phone':unicode,
      'credit_cards':list
  }
  use_dot_notation = True

class CreditCard(Document):
  __collection__ = 'credit_cards'
  structure = {
      'number':unicode,
      'code':unicode,
      'exp_month':unicode,
      'exp_year':unicode,
      'first_name':unicode,
      'last_name':unicode,
      'street':unicode,
      'city':unicode,
      'zip':unicode,
      'state':unicode
  }
  use_dot_notation = True

