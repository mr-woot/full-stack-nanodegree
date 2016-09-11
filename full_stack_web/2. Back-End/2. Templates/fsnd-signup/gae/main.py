import os
import re
import webapp2
import jinja2

# Template dirs
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# Regular expressions
username_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
password_re = re.compile("^.{3,20}$")
email_re = re.compile("^[\S]+@[\S]+.[\S]+$")

# authentification - functions


def valid_username(username):
    return username and username_re.match(username)


def valid_password(password):
    return password and password_re.match(password)


def valid_email(email):
    return not email or email_re.match(email)

# Main handler that renders content


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Gae(Handler):

    def get(self):
        self.render("index.html")

    def post(self):
        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        params = dict(username=username, password=password)
        if not valid_username(username):
            params['u_error'] = "That's not a valid username."
            error = True
        if not valid_password(password):
            params['p_error'] = "That's wasn't a valid password."
            error = True
        elif password != verify:
            params['v_error'] = "Your passwords didn't match."
            error = True
        if not valid_email(email):
            params['e_error'] = "That's not a valid email"
            error = True
        if error:
            self.render("index.html", **params)
        else:
            self.redirect("/welcome?username=" + username)


class Welcome(Handler):

    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.render("welcome.html", username=username)
        else:
            self.redirect("index.html")
app = webapp2.WSGIApplication([
    ('/', Gae), ('/welcome', Welcome)
],
    debug=True)
