from google.appengine.ext import db

from user import User
import jinja_helper


class Post(db.Model):
    """
        Post Class contains the blog post information.
    """
    user_id = db.IntegerProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def getUserName(self):
        """
            Gets username of the blog post created.
        """
        user = User.by_id(self.user_id)
        return user.name

    def render(self):
        """
            Renders the post of Object data
        """
        self._render_text = self.content.replace('\n', '<br>')
        return jinja_helper.render_str("post.html", p=self)
