"""
MongoDB document models.
"""

__author__ = 'Cory Li (coryli@mit.edu), Justin Venezuela (jven@mit.edu)'

from flaskext.mongokit import Document

class User(Document):
  __collection__ = 'users'
  # TODO(jven): UNICODE!!!!!!!!
  structure = {
      'first_name':str,
      'last_name':str,
      'email':str,
      'password':str,
      'address':str,
      'credit_card_number':int,
      'credit_card_code':int,
      'credit_card_exp_month':int,
      'credit_card_exp_year':int
  }
  use_dot_notation = True
