from flask import Flask
from flask_cas import CAS
import config
import os 

dir = os.path.abspath('orangepages/templates')
app = Flask(__name__, template_folder=dir)
cas = CAS(app, '/cas')
app.config.from_object(config.Config)

# Import and register views.
from orangepages.views import general, post, search, user, test
blueprints = [general, post, search, user, test]
for bp in blueprints:
    app.register_blueprint(bp.page)
