from flask import Flask
import config
app = Flask(__name__)
app.config.from_object(config.Config)


# Import and register views.
from orangepages.views import general, post, search, user, test
blueprints = [general, post, search, user, test]
for bp in blueprints:
    app.register_blueprint(bp.page)
