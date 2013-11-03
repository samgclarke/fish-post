from flask import Flask
from mongoengine import connect

app = Flask(__name__)
app.debug = True
app.config["SITE_URL"] = 'http://freak-post.herokuapp.com'

app.config["MONGODB_DB"] = 'app14198794'
connect(
    'app14198794',
    username='heroku',
    password='3_GdcuX1W7oH=',
    host='mongodb://heroku:3_GdcuX1W7oH=@alex.mongohq.com:10095/app14198794',
    port=10095
)
