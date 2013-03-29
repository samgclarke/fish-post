from flask import Blueprint, request, redirect, render_template, url_for, \
    session, g, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from functools import wraps
import os

from flask.ext.openid import OpenID
from forms import LoginForm
from config import OPENID_PROVIDERS
from models import User, ROLE_USER

app = Flask(__name__)
from mongo_log.models import Post, Comment


posts = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):

    #decorators = [login_required]

    def get(self):
        p = Post.objects.all()
        return render_template('posts/list.html', posts=p)


posts.add_url_rule('/', view_func=ListView.as_view('list'))
