from flask import Flask
from mongoengine import connect

app = Flask(__name__)
app.debug = True


app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
