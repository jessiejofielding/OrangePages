from flask import Flask
from flask_cas_fix import CAS
import config
import os 

dir = os.path.abspath('orangepages/templates')
app = Flask(__name__, template_folder=dir)
cas = CAS(app, '/cas')
app.config.from_object(config.Config)

# Import and register views.
from orangepages.views import general, post, search, user, error, test
blueprints = [general, post, search, user, error, test]
for bp in blueprints:
    app.register_blueprint(bp.page)
