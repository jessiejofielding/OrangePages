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

app.run(host='0.0.0.0', port=5000, debug=True)

# from orangepages.views.test_local import add_tag, search_tag
#
# add_tag('zkoh', "tag1")
# search_tag("tag1")

# from orangepages.views.test import add_friend_local, unfriend_local, get_friends_local
# from orangepages.views.test import is_friend_of
#
# add_friend_local('jexample', 'sstudent')
# # add_friend_local('jexample', 'zkoh')
#
# friend_list = get_friends_local('jexample')
# for x in friend_list:
#     print("john's friend: ", x.uid)
#
# friend_list = get_friends_local('sstudent')
# for x in friend_list:
#     print("sstudent's friend: ", x.uid)
#
# ans = is_friend_of('jexample', 'sstudent')
# print("john n sally friends? ", ans)
#
# print("john unfriends sally")
# unfriend_local('jexample', 'sstudent')
#
# ans = is_friend_of('jexample', 'sstudent')
# print("john n sally friends? ", ans)

# friend_list = get_friends_local('jexample')
# for x in friend_list:
#     print("john's friend: ", x.uid)
#
# friend_list = get_friends_local('sstudent')
# for x in friend_list:
#     print("sstudent's friend: ", x.uid)


# unfriend_local('jexample', 'sstudent')
# likers_local(2)
# like_local('jexample', 2, True)
# likers_local(2)
# testsearch_local("elise")
