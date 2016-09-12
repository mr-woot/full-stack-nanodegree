import os
import webapp2
import jinja2
from google.appengine.ext import db

# Template dirs

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# Regular expressions for authentification

username_re = "^[a-zA-Z0-9_-]{3,20}$"
password_re = "^.{3,20}$"
email_re = "^[\S]+@[\S]+.[\S]+$"

# Main handler that renders content


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class AsciiChan(Handler):

    def render_chan(self, t_error="", a_error="", title="", art=""):
        arts = db.GqlQuery("select * from Art order by created desc")
        self.render("index.html", t_error=t_error,
                    a_error=a_error, title=title, art=art, arts=arts)

    def get(self):
        self.render_chan()

    def post(self):
        error = False
        title = self.request.get("title")
        art = self.request.get("art")
        t_error = ""
        a_error = ""
        if not title:
            t_error = "Wanna go without title, well not in my app"
            error = True
        if not art:
            a_error = "It's not going without art, chica"
            error = True
        if error:
            self.render_chan(t_error, a_error, title, art)
        elif title and art:
            a = Art(title=title, art=art)
            a.put()
            self.redirect("/")
app = webapp2.WSGIApplication([
    ('/', AsciiChan)],
    debug=True)
