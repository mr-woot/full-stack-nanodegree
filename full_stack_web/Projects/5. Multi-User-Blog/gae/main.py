import re
import hmac

import webapp2

from google.appengine.ext import db


from model import Comment
from model import Like
from model import Post
from model import User

import jinja_helper

# hashing secret

secret = "haha_u_wanna_know_secret"


def make_secure_val(val):
    """
        Makes the value secure
    """
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """
        Checks the value, if it is secure or not
    """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


# Regex for input validation

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{5,20}$")
PASS_RE = re.compile(r"^.{5,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_username(username):
    """
        Validates username
    """
    return username and USER_RE.match(username)


def valid_password(password):
    """
        Validates password
    """
    return password and PASS_RE.match(password)


def valid_email(email):
    """
        Validates email
    """
    return not email or EMAIL_RE.match(email)


# Main Handler


class Handler(webapp2.RequestHandler):
    """
        Main Handler class that provides helper methods
    """

    def write(self, *a, **kw):
        """
            Outputs to the browser
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
            Renders html using template
        """
        params['user'] = self.user
        return jinja_helper.render_str(template, **params)

    def render(self, template, **kw):
        """
            Writes the rendered content to browser
        """
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """
            Set the secure cookie header
        """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """
            Reads the secure cookie
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """
            Sets the cookie at the time of login
        """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """
            Unset the cookie to null at the time of logout
        """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """
            Executed every time on all pages, that verifies login, logout, cookie
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


# Main Page


class MainPage(Handler):

    def get(self):
        self.render("index.html")

# Signup handler


class Signup(Handler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

# Register User


class Register(Signup):

    def done(self):
        # check whether user exists or not
        u = User.by_name(self.username)

        if u:
            msg = 'Voila, don\'t fool around here, need to register'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/welcome')

# Login module


class Login(Handler):

    def get(self):
        """
            Checks if user cookie not available, then redirects to login page.
        """
        if not self.user:
            self.render('login-form.html')
        else:
            self.redirect('/welcome')

    def post(self):
        """
            gets username, email and password attrs.
        """
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Login Invalid'
            self.render('login-form.html', error=msg)

# Logout module


class Logout(Handler):

    def get(self):
        """
            logouts the session
        """
        self.logout()
        self.redirect('/login')

# Welcome module


class Welcome(Handler):

    def get(self):
        """
            Welcome the user when logged in(displayed only for 2 seconds)
        """
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/welcome')


# Blog Parent key


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

# Front Blog module


class BlogFront(Handler):

    def get(self):
        """
            Main Blog Page with all posts sorted
        """
        deleted_post_id = self.request.get('deleted_post_id')
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts,
                    deleted_post_id=deleted_post_id)

# Post Page module


class PostPage(Handler):

    def get(self, post_id):
        """
            Post Page with content and also comments and likes too.
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        comments = db.GqlQuery(
            "select * from Comment where post_id=" + post_id + " order by created desc")

        likes = db.GqlQuery("select * from Like where post_id=" + post_id)

        if not post:
            self.error(404)
            return
        error = self.request.get('error')

        self.render("permalink.html", post=post,
                    no_of_likes=likes.count(),
                    comments=comments, error=error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        """
            While commenting, a comment datastore object is created and stored,
            with respect to each user and post.
        """
        c = ""
        if(self.user):
            # On clicking like, post-like value increases.
            if(self.request.get('like') and
               self.request.get('like') == "update"):
                likes = db.GqlQuery("select * from Like where post_id= " +
                                    post_id + " and user_id= " +
                                    str(self.user.key().id()))

                if self.user.key().id() == post.user_id:
                    self.redirect("/blog/" + post_id +
                                  "?error= You cannot like your own post")
                    return
                elif likes.count() == 0:
                    l = Like(parent=blog_key(), user_id=self.user.key().id(),
                             post_id=int(post_id))
                    l.put()

            # On commenting, it creates new comment tuple
            if(self.request.get('comment')):
                c = Comment(parent=blog_key(), user_id=self.user.key().id(),
                            post_id=int(post_id),
                            comment=self.request.get('comment'))
                c.put()
        else:
            self.redirect("/blog/" + post_id +
                          "?error= Need to Login Please.")
            return

        comments = db.GqlQuery("select * from Comment where post_id = " +
                               post_id + "order by created desc")

        likes = db.GqlQuery("select * from Like where post_id=" + post_id)

        self.render("permalink.html", post=post,
                    comments=comments, no_of_likes=likes.count(),
                    new=c)


class NewPost(Handler):

    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        """
            Creates new post and redirects to it
        """
        if not self.user:
            self.redirect('/login')
        else:
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                p = Post(parent=blog_key(), user_id=self.user.key().id(),
                         subject=subject, content=content)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                error = "subject and content, please!"
                self.render("newpost.html", subject=subject,
                            content=content, error=error)


class DeletePost(Handler):

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.user_id == self.user.key().id():
                post.delete()
                self.redirect("/?deleted_post_id=" + post_id)
            elif post.user_id != self.user.key().id():
                self.redirect("/blog/" + post_id +
                              "?error= Access denied")
        else:
            self.redirect("/blog/" + post_id +
                          "?error= Cannot Delete, Login Please.")


class EditPost(Handler):

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.user_id == self.user.key().id():
                self.render("editpost.html", subject=post.subject,
                            content=post.content)
            else:
                self.redirect("/blog/" + post_id +
                              "?error= Access denied")
        else:
            self.redirect("/blog/" + post_id +
                          "?error= Login Please.")

    def post(self, post_id):
        """
            Updates post
        """
        if not self.user:
            self.redirect('/login')
            return
        else:
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                key = db.Key.from_path('Post', int(post_id),
                                       parent=blog_key())
                post = db.get(key)
                if post.user_id == self.user.key().id():
                    post.subject = subject
                    post.content = content
                    post.put()
                    self.redirect('/blog/' + post_id)
                elif post.user_id != self.user.key().id():
                    self.redirect("/login")
            else:
                error = "subject and content, please!"
                self.render("editpost.html", subject=subject,
                            content=content, error=error)


class DeleteComment(Handler):

    def get(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id),
                                   parent=blog_key())
            c = db.get(key)
            if c.user_id == self.user.key().id():
                c.delete()
                self.redirect("/blog/" + post_id +
                              "?deleted_comment_id=" + comment_id)
            elif c.user_id != self.user.key().id():
                self.redirect("/blog/"
                              + post_id + "?error= Access Denied")
        else:
            self.redirect("/blog/"
                          + post_id + "?error= Login Please.")


class EditComment(Handler):

    def get(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id),
                                   parent=blog_key())
            c = db.get(key)
            if c.user_id == self.user.key().id():
                self.render("editcomment.html", comment=c.comment)
            elif c.user_id != self.user.key().id():
                self.redirect("/blog/" + post_id +
                              "?error= Access Denied.")
        else:
            self.redirect("/blog/" + post_id +
                          "?error= Login Please.")

    def post(self, post_id, comment_id):
        """
            Updates post.
        """
        if not self.user:
            self.redirect("/blog/" + post_id +
                          "?error= Login Please.")
            return

        else:
            comment = self.request.get('comment')

            if comment:
                key = db.Key.from_path('Comment',
                                       int(comment_id), parent=blog_key())
                c = db.get(key)
                if c.user_id != self.user.key().id():
                    self.redirect("/blog/" + post_id +
                                  "?error= Login Please.")
                c.comment = comment
                c.put()
                self.redirect('/blog/%s' % post_id)
            else:
                error = "subject and content, please!"
                self.render("editpost.html", subject=subject,
                            content=content, error=error)


app = webapp2.WSGIApplication([
    ('/', BlogFront),
    ('/welcome', Welcome),
    ('/blog', BlogFront),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/newpost', NewPost),
    ('/blog/editpost/([0-9]+)', EditPost),
    ('/blog/deletepost/([0-9]+)', DeletePost),
    ('/blog/editcomment/([0-9]+)/([0-9]+)',
     EditComment),
    ('/blog/deletecomment/([0-9]+)/([0-9]+)',
     DeleteComment),
    ('/signup', Register),
    ('/login', Login),
    ('/logout', Logout)],
    debug=True)
