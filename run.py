import os
from orangepages import app, admin

from flask_admin.contrib.sqla import ModelView
from orangepages.models.models import db, User, Post, Relationship, Group, Comment, Tag, Notification

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Relationship, db.session))
admin.add_view(ModelView(Notification, db.session))

temp = os.environ.get('PORT')

app.run(host='0.0.0.0', port=int(temp))
