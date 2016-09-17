import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

# Template dirs
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# # Regular expressions for authentification
# username_re = "^[a-zA-Z0-9_-]{3,20}$"
# password_re = "^.{3,20}$"
# email_re = "^[\S]+@[\S]+.[\S]+$"

# Main handler that renders content


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

# blog

# important for having as a common parent to all blog posts, very handy


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)


class BlogFront(Handler):

    def get(self):
        posts = Post.all().order('-created')
        self.render("index.html", posts=posts)


class PostPage(Handler):

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
        self.render("permalink.html", post=post)


class BlogPost(Handler):

    def get(self):
        self.render("add_post.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content)
            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("add_post.html", subject=subject,
                        content=content, error=error)

# class BlogPost(Handler):
#
#     def render_post(self, s_error="", c_error="", subject="", content=""):
#         self.render("add_post.html", s_error=s_error,
# c_error=c_error, subject=subject, content=content)
#
#     def get(self):
#         self.render_post()
#
        # def post(self):
        # error = False
        # subject = self.request.get("subject")
        # content = self.request.get("content")
        # s_error = ""
        # c_error = ""
        # if not subject:
        #     s_error = "Wanna go without subject, well not in my app"
        #     error = True
        # if not content:
        #     c_error = "It's not going without content, chica"
        #     error = True
        # if error:
        #     self.render_post(s_error, c_error, subject, content)
#         elif content and subject:
#             p = Post(subject=subject, content=content)
#             p.put()
#             self.redirect("/blog")
#
# class Blog(Handler):
#
#     def get(self):
#         posts = db.GqlQuery("select * from Post order by created desc")
#         self.render("index.html", posts=posts)


app = webapp2.WSGIApplication([
    ('/', BlogFront),
    ('/?', BlogFront),
    ('/newpost', BlogPost),
    ('/([0-9]+)', PostPage)],
    debug=True)
