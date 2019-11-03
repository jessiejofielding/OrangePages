from flask import Flask
app = Flask(__name__)


# Import and register views.
from orangepages.views import general, post, user, testsearch
app.register_blueprint(general.page)
app.register_blueprint(post.page)
app.register_blueprint(user.page)
app.register_blueprint(testsearch.page)