#!/usr/bin/env python
from flask.ext.mongoengine import MongoEngine
from config import app
import os

app.secret_key = 'teddymonkey'

# wrap app in mongengine
db = MongoEngine(app)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.debug = True

    app.run(host='0.0.0.0', port=port)
