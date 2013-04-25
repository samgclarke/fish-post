import datetime
from application import db
from flask import url_for


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

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % (self.username)


class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    author = db.ReferenceField(User)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }


class BlogPost(Post):
    body = db.StringField(required=True)


class Video(Post):
    embed_code = db.StringField(required=True)


class Image(Post):
    image_url = db.StringField(required=True, max_length=255)


class Quote(Post):
    body = db.StringField(required=True)
    author = db.StringField(
        verbose_name="Author Name", required=True, max_length=255
    )


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
