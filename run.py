import os
from orangepages import app, admin

from flask_admin.contrib.sqla import ModelView
from orangepages.models.models import db, User, Post, Relationship, Group, Comment, Tag, Notification

import orangepages.views.util as util
from flask_admin.contrib import sqla

class ModelView(sqla.ModelView):

    def is_accessible(self):
        if util.cur_user() is None:
            return False

        if util.cur_uid() in ['jjf4', 'jamieguo', 'zkoh', 'ccolter', 'jkallini']:
            return True

        return False
        

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect("orangepages.herokuapp.com")


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Relationship, db.session))
admin.add_view(ModelView(Notification, db.session))

temp = os.environ.get('PORT')

app.run(host='0.0.0.0', port=int(temp))
