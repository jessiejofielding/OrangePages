from flask import Flask
from flask_cas_fix import CAS
import config
import os
import cloudinary as Cloud
from dotenv import load_dotenv
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

dotenv_path = os.path.join("./", 'dev.env')
load_dotenv(dotenv_path)

dir = os.path.abspath('orangepages/templates')
app = Flask(__name__, template_folder=dir)

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        title = 'Hello'
        return self.render('admin.html', title=title, message=title)

admin = Admin(app, index_view=MyHomeView())
# admin = Admin(app, name='DatabaseView', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Post, db.session))
cas = CAS(app, '/cas')
app.config.from_object(config.Config)

# print(os.environ.get('CLOUDINARY_CLOUD_NAME'))
# Cloud.config(
#   cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME') ,
#   api_key = os.environ.get('CLOUDINARY_API_KEY') ,
#   api_secret = os.environ.get('CLOUDINARY_API_SECRET')
# )

# Import and register views.
from orangepages.views import general, post, search, user, error, friend
blueprints = [general, post, search, user, error, friend]
for bp in blueprints:
    app.register_blueprint(bp.page)
