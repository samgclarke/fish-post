import requests

from flask import Blueprint, request, redirect, render_template, \
    url_for, session, g
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from mongo_log.views import login_required
from mongo_log.models import Post, BlogPost, \
    Video, Image, Link, User

from config import app


# send mail function
def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests.post(
        "https://api.mailgun.net/v2/%s/messages" % app.config[
            'MAILGUN_DOMAIN'],
        auth=("api", app.config['MAILGUN_KEY']),
        data={
            "from": from_address,
            "to": to_address,
            "subject": subject,
            "text": plaintext,
            "html": html
        }
    )
    return r


admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [login_required]

    cls = Post

    def get(self):
        posts = self.cls.objects.filter(author=g.user)
        return render_template('admin/list.html', posts=posts)


class Detail(MethodView):

    decorators = [login_required]

    # Map post types to models
    class_map = {
        # 'post': BlogPost, # disabled for now
        'video': Video,
        'image': Image,
        'link': Link,
    }

    def get_context(self, slug=None):

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            # Handle old posts types as well
            cls = post.__class__ if post.__class__ != Post else BlogPost
            form_cls = model_form(
                cls, exclude=('created_at', 'comments', 'author'))
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)
        else:
            # Determine which post type we need
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(
                cls, exclude=('created_at', 'comments', 'author'))
            form = form_cls(request.form)
        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.author = g.user
            post.save()

            url = url_for('posts.detail', slug=post.slug)

            # get list of user emails
            users = User.objects.all()
            recipients_list = []
            for user in users:
                recipients_list.append(user.email)

            # send email notification to all users
            send_mail(
                to_address=recipients_list,
                from_address='freakpost-app@gmail.com',
                subject='New Post on Fish Post!',
                plaintext='Someone just posted something on Fish Post.',
                html='Someone just posted something on Fish Post. <br /><b><a href="' + app.config["SITE_URL"] + url + '">Link</a></b>'
            )

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.hml', **context)


class Delete(MethodView):

    def get(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        post.delete()
        return render_template('admin/delete.html', post=post)


# register urls
admin.add_url_rule(
    '/admin/',
    view_func=List.as_view('index')
)
admin.add_url_rule(
    '/admin/create/',
    defaults={'slug': None},
    view_func=Detail.as_view('create')
)
admin.add_url_rule(
    '/admin/<slug>/',
    view_func=Detail.as_view('edit')
)
admin.add_url_rule(
    '/admin/delete/<slug>/',
    view_func=Delete.as_view('delete')
)
