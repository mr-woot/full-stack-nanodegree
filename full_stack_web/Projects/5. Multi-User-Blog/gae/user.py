import random
import hashlib

from string import letters
from google.appengine.ext import db

# Helper functions

# Returns random word comprising of letters


def make_salt(length=10):
    return ''.join(random.choice(letters) for x in xrange(length))

# Returns hashed value of the password


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (salt, h)

# Checks whether the password is valid or not


def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)

# User Key model


def users_key(group='default'):
    return db.Key.from_path('users', group)

# Main User Model


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """
            Get the User object from datastore by user_id.
        """
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """
            Get the User object from datastore by name.
        """
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """
            Registers the new user into the datastore.
        """
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """
            Login as a user.
        """
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
