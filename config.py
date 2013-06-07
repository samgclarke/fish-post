from flask import Flask
from flask import Blueprint
from mongoengine import connect

app = Flask(__name__)
app.debug = True


#app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"


app.config["MONGODB_DB"] = 'app14198794'
connect(
    'app14198794',
    username='heroku',
    password='a614e68b445d0d9d1c375740781073b4',
    host='mongodb://heroku:a614e68b445d0d9d1c375740781073b4@alex.mongohq.com:10095/app14198794',
    port=10095
)


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
