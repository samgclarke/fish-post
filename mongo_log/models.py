import datetime
from flask import url_for
from application import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.DynamicDocument):
    #openid = db.IntField(primary_key=True)
    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    role = db.IntField(default=ROLE_USER)

    # speifics for OpenID
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #def get_id(self):
    #    return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
