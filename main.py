import os
import webapp2
import jinja2

# Template dirs
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# Regular expressions for authentification
username_re = "^[a-zA-Z0-9_-]{3,20}$"
password_re = "^.{3,20}$"
email_re    = "^[\S]+@[\S]+.[\S]+$"

# Main handler that renders content
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class gae(Handler):
    def get(self):
        self.render("index.html")
    def post(self):
    	text = self.request.get("text")
        self.render("index.html", text=text)

app = webapp2.WSGIApplication([
    ('/', gae)],
    debug=True)

