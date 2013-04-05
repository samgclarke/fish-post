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

from config import app
from mongo_log.models import Post, Comment


############################ OPENID ######################
basedir = os.path.abspath(os.path.dirname(__file__))
oid = OpenID(app, os.path.join(basedir, 'tmp'))

#@lm.user_loader
#def load_user(id):
#    return User.query.get(int(id))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/success', methods=['GET', 'POST'])
def success():
    return "success!"


@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = User.objects.get_or_404(email=session['email'])


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('posts.list'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(
            form.openid.data, ask_for=['nickname', 'email']
        )
    return render_template(
        'login.html',
        next=oid.get_next_url(),
        error=oid.fetch_error(),
        title='Sign In',
        form=form,
        providers=OPENID_PROVIDERS
    )


@oid.after_login
def after_login(resp):
    # if fields empty, flash error message
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    try:
        # get user object based on request
        user = User.objects.get(email=resp.email)
    except User.DoesNotExist:
        return redirect(url_for('login'))
    """
    if user is None:
        username = resp.nickname
        if username is None or username == "":
            username = resp.email.split('@')[0]
        user = User(username=username, email=resp.email, role=ROLE_USER)
        session['username'] = username

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    return redirect(request.args.get('next') or url_for('admin.list'))
    """
    session['user'] = user
    session['email'] = resp.email
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    else:
        flash(u'Your credentials have not been recognized')
        return redirect(url_for('login'))
    return redirect(url_for('success', next=oid.get_next_url(),
                            username=resp.nickname,
                            email=resp.email))


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember_me', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())
############################ OPENID ######################


############################ POSTS  ######################
posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):

    #decorators = [login_required]

    def get(self, page=1):
        if request.args.get('page'):
            page = int(request.args.get('page'))
        posts = Post.objects.paginate(page=page, per_page=10)
        #raise Exception
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    #decorators = [login_required]

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)


# register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>', view_func=DetailView.as_view('detail'))
