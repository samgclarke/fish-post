#!/usr/bin/env python
from flask.ext.mongoengine import MongoEngine
from config import app
import os

app.secret_key = 'teddymonkey'

# get config settings
#if __name__ == '__main__':
#    app.config.from_object('config')
#else:
#    app.config.from_object('heroku_config')
app.config.from_object('config')

# wrap app in mongengine
db = MongoEngine(app)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.debug = True

    app.run(host='0.0.0.0', port=port)
