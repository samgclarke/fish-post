from flask import Flask
from flask import Blueprint
from mongoengine import connect

app = Flask(__name__)
app.debug = True

app.config["SITE_URL"] = 'http://fish-post.herokuapp.com'

#app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"


app.config["MONGODB_DB"] = 'heroku_app20627519'
connect(
    'heroku_app20627519',
    username='heroku_app20627519',
    password='fish2014',
    host='mongodb://heroku_app20627519:fish2014@ds061238.mongolab.com:61238/heroku_app20627519',
    port=10095
)

# email server
app.config['MAILGUN_KEY'] = 'key-3z8y4qxoz2cbkgaf2k5gier1ytx9wg14'
app.config['MAILGUN_DOMAIN'] = 'app14198794.mailgun.org'


CSRF_ENABLED = True
SECRET_KEY = 'teddymonkey'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


###########################
### register blueprints ###
###########################
def register_blueprints(app):
    # prevents circular imports
    from mongo_log.views import posts
    from mongo_log.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)
