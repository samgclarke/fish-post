#!/usr/bin/env python
import os
import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine, mongoengine
from mongoengine import connect


app = Flask(__name__)
app.config["MONGODB_DB"] = ''
connect(
    '',
    username='heroku',
    password='',
    host='',
    port=
)
db = MongoEngine(app)


class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(max_length=255, required=True)


@app.route('/')
def hello_world():
    posts = Post.objects.all()
    return 'Hello Mongo! Read this: ' + posts[0].body

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
