import os
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


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class BlogPost(Handler):

    def render_post(self, s_error="", c_error="", subject="", content=""):
        self.render("add_post.html", s_error=s_error,
                    c_error=c_error, subject=subject, content=content)

    def get(self):
        self.render_post()

    def post(self):
        error = False
        subject = self.request.get("subject")
        content = self.request.get("content")
        s_error = ""
        c_error = ""
        if not subject:
            s_error = "Wanna go without subject, well not in my app"
            error = True
        if not content:
            c_error = "It's not going without content, chica"
            error = True
        if error:
            self.render_post(s_error, c_error, subject, content)
        elif content and subject:
            p = Post(subject=subject, content=content)
            p.put()
            self.redirect("/blog")


class Blog(Handler):

    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc")
        self.render("index.html", posts=posts)


app = webapp2.WSGIApplication([
    ('/', Blog),
    ('/blog', Blog),
    ('/post', BlogPost)],
    debug=True)
