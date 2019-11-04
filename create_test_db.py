from orangepages.models.models import db, User, app, Group, Post
import orangepages.models.statuses as st

# hard coding that this will only work on my computer in the test db so that we 
# don't accidentally drop_all() and replace with this mess on an important db
# I haven't figured out how to do it with a relative path yet but will figure 
# that out soon 
if app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite:////Users/jessie/OrangePages/test.sqlite':
    exit()

# this is so that we can mess around with different possibilities for testing
# without having to think about what already exists
# once we have a test db that we like, we won't run this anymore so we won't keep
# dropping and creating the whole db 
db.drop_all()
db.create_all()
db.session.commit()

# Make some students, some groups, some posts
sally = User('sstudent', 'Sally', 'Student', 'sstudent@princeton.edu')
john = User('jexample', 'John', 'Example', 'jexample@princeton.edu')
cos333 = Group('COS333', None, [sally])
sally_friends = Group('Friends', sally, [])
post1 = Post("Hey everyone! It's my first post :))))", sally, [cos333, sally_friends])

cos333.add_member(john)
# cos333.remove_member(sally)
db.session.add(sally)
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
    print(user.posts_made)
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
    print(post.creator)
    print(post.content)
    print(post.groups)
    print()

