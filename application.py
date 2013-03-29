#!/usr/bin/env python
import os
import datetime
from flask import Flask, url_for
from flask.ext.mongoengine import MongoEngine, mongoengine
from mongoengine import connect

from config import app

# get config settings
if __name__ == '__main__':
    app.config.from_object('config')
else:
    app.config.from_object('heroku_config')


db = MongoEngine(app)


@app.route('/')
def hello_world():
    return 'Hello Mongo: '


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
