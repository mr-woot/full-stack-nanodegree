import os
import webapp2
import jinja2
import hmac

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


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()

    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

# For hashing string

SECRET = "WANnAhAckmE"


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


# Making secure has in the form (val,hash(val))


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


# Checking whether returned value of hash is correct or not


def check_secure_val(s):
    val = s.split('|')[0]
    if make_secure_val(val) == s:
        return val


# Main Page Handler


class MainPage(Handler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        if visit_cookie_str:
            cookie_val = check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits = visits + 1

        new_cookie_val = make_secure_val(str(visits))

        self.response.headers.add_header(
            'Set-Cookie', 'visits=%s' % new_cookie_val)

        if visits > 1000:
            self.write("You did it, amazing....Did you cheat?")
        else:
            self.write("You visited %s times" % visits)

    # def post(self):
    #     text = self.request.get("text")
    #     self.render("index.html", text=text)

# Application Routes


app = webapp2.WSGIApplication([
    ('/', MainPage)],
    debug=True)
