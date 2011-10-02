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
      'zip':unicode,
      'state':unicode,
      'phone':unicode,
      'credit_card_number':unicode,
      'credit_card_code':unicode,
      'credit_card_exp_month':unicode,
      'credit_card_exp_year':unicode
  }
  use_dot_notation = True
