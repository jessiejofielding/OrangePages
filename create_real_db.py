from orangepages.models.models import db, User, app, Group, Post
import orangepages.models.statuses as st
import config


#if we want to reset, we can db.drop_all()
db.drop_all()
db.create_all()
db.session.commit()

public = Group('Public', None, [])
db.session.add(public)
db.session.commit()