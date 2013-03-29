from flask import Flask

app = Flask(__name__)
app.debug = True


app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

"""
app.config["MONGODB_DB"] = 'app14198794'
connect(
    'app14198794',
    username='heroku',
    password='a614e68b445d0d9d1c375740781073b4',
    host='mongodb://heroku:a614e68b445d0d9d1c375740781073b4@alex.mongohq.com:10095/app14198794',
    port=10095
)
"""