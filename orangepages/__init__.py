from flask import Flask
from flask_cas_fix import CAS
import config
import os
import cloudinary as Cloud
from dotenv import load_dotenv

dotenv_path = os.path.join("./", 'dev.env')
load_dotenv(dotenv_path)

dir = os.path.abspath('orangepages/templates')
app = Flask(__name__, template_folder=dir)
cas = CAS(app, '/cas')
app.config.from_object(config.Config)

Cloud.config(
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME') ,
  api_key = os.environ.get('CLOUDINARY_API_KEY') ,
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

# Import and register views.
from orangepages.views import general, post, search, user, error, test, friend
blueprints = [general, post, search, user, error, test, friend]
for bp in blueprints:
    app.register_blueprint(bp.page)
