from orangepages.models.models import db, User, app, Group, Post
import config

if app.config['SQLALCHEMY_DATABASE_URI'] != config.SQLALCHEMY_DATABASE_URI:
    print("db already exists")
    exit()

db.drop_all()
db.create_all()
db.session.commit()

# Make some students, some groups, some posts
sally = User('sstudent', 'Sally', 'Student', 'sstudent@princeton.edu')
sally2 = User('ssam', 'Sally', 'Sam', 'ssam@princeton.edu')
sally3 = User('ssally', 'Sam', 'Sally', 'ssally@princeton.edu')

john = User('jexample', 'John', 'Example', 'jexample@princeton.edu')
cos333 = Group('COS333', None, [sally])
sally_friends = Group('Friends', sally, [])
post1 = Post("Hey everyone! It's my first post :))))", sally, [cos333, sally_friends])

cos333.add_member(john)
# cos333.remove_member(sally)
db.session.add(sally)
db.session.add(sally2)
db.session.add(sally3)
db.session.add(john)
db.session.add(cos333)
db.session.add(post1)
db.session.add(sally_friends)
db.session.commit()

users = User.query.all()
for user in users:
    print(user.firstname)
    print(user.lastname)
    print(user.uid)
    for group in user.groups_in.all():
        print(group.title)
    print()

print()

groups = Group.query.all()
for group in groups:
    print(group.title)
    print(group.members)
    print()

print()

posts = Post.query.all()
for post in posts:
    print(post.creatorid)
    print(post.content)
    print(post.groups)
    print()
