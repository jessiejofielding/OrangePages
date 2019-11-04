from flask import Flask
app = Flask(__name__)


# Import and register views.
from orangepages.views import general, post, search, user, test
blueprints = [general, post, search, user, test]
for bp in blueprints:
    app.register_blueprint(bp.page)
