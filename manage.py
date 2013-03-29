#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server

from config import app
manager = Manager(app)


if __name__ == '__main__':  
    # Turn on debugger by default and reloader
    port = int(os.environ.get('PORT', 5000))
    manager = Manager(app)
    manager.add_command("runserver", Server(
        use_debugger = True,
        use_reloader = True,
        host = '0.0.0.0',
        port=port)
    )
    manager.run()