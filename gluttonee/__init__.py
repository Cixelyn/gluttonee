"""
Gluttonee web application.
"""

__author__ = 'Cory Li (coryli@mit.edu), Justin Venezuela (jven@mit.edu)'

from flask import Flask

app = Flask(__name__)

@app.before_request
def before_request():
  pass

@app.route('/')
def home():
  return 'Hello world!'

if __name__ == '__main__':
  app.run(debug=True)
