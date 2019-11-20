from orangepages.models.models import db, User, app, Group, Post
import orangepages.models.statuses as st
from orangepages.views.test import add_friend_local
from orangepages.views.test_local import add_tag, search_tag
import config

# hard coding this so that create_test_db can't mess with real db
if app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite:///../test.sqlite':
    print("not test db")
    exit()

# this is so that we can mess around with different possibilities for testing
# without having to think about what already exists
# once we have a test db that we like, we won't run this anymore so we won't keep
# dropping and creating the whole db

db.drop_all()
db.create_all()
db.session.commit()

public = Group('Public', None, [])
db.session.add(public)
db.session.commit()

# Make some students, some groups, some posts
sally = User('sstudent', 'Sally', 'Student', 'sstudent@princeton.edu')
sally2 = User('ssam', 'Sally', 'Sam', 'ssam@princeton.edu')
sally3 = User('ssally', 'Sam', 'Sally', 'ssally@princeton.edu')
john = User('jexample', 'John', 'Example', 'jexample@princeton.edu')

elise = User('ccolter', 'Elise', 'Colter', 'ccolter@princeton.edu')
jessie = User('jjf4', 'Jessica', 'Fielding', 'jjf4@princeton.edu')
julie = User('jkallini', 'Julie', 'Kallini', 'jkallini@princeton.edu')
# jamie = User('jamieguo', 'Jamie', 'Guo', 'jamieguo@princeton.edu')
zexin = User('zkoh', 'Ze-Xin', 'Koh', 'zkoh@princeton.edu')

batman = User('bmcman', 'Bat', 'McMan', 'bmcman@princeton.edu')
dan = User('dmiller', 'Dan', 'Miller', 'dmiller@princeton.edu')

# users = [sally, sally2, sally3, john, elise, jessie, julie, jamie, zexin, batman, dan]
users = [sally, sally2, sally3, john, elise, jessie, julie, zexin, batman, dan]


cos333 = Group('COS333', None, [sally])
the_clique = Group('Clique', None, [sally])
post1 = Post("Hey everyone! It's my first post :))))", sally, [cos333, the_clique])
post2 = Post("Hey everyone! It's the second post :))))", sally, [cos333])
post5 = Post("Hey so I just really wanted to let everyone know that our 333 project (Orange Pages :) ) is in development! Hope you'll all like it!!", jessie, [cos333])
post3 = Post("Hey everyone! It's my third post :))))", sally, [the_clique])
post4 = Post("Hey everyone! It's my fourth post :))))", sally, [cos333])
post6 = Post("I'm really bad at writing posts but I want there to be some variety on this feed is all!", jessie, [cos333])

posts = [post1, post2, post3, post4, post5, post6]
cos333.add_member(john)
the_clique.add_member(john)
post1.add_like(john)
# cos333.remove_member(sally)

for user in users:
    public.add_member(user)
    db.session.add(user)


db.session.add(cos333)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.commit()


users = User.search("s")
# users = User.query.all()
for user in users:
    print(user.firstname)
    print(user.lastname)
    print(user.uid)
    print(user._posts_made)
    for group in user.groups_in.all():
        print(group.title)
    print()

print()

# groups = Group.query.all()
# for group in groups:
#     print(group.title)
#     print(group.members)
#     print()

# print()

# posts = Post.query.all()
# for post in posts:
#     print(post.creatorid)
#     print(post.creator)
#     print(post.content)
#     print(post.groups)
#     print()

feed = john.get_feed()

print(feed)

# sally2.update_info('Sallie', 'Sam', 'ssam@princeton.edu')
elise.update_optional_info("Elise", "Colter", "ccolter@princeton.edu",
"Nashville", "Tennessee", "U.S.", "2021", "COS", "N/A", "Little")
db.session.commit()

for like in post1.likes:
    print(like.firstname)

# import cloudinary
# import os
# from cloudinary.uploader import upload

# cloudinary.config.update = ({
#     'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
#     'api_key': os.environ.get('CLOUDINARY_API_KEY'),
#     'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
# })

# tig = upload('/Users/jessie/OrangePages/tiger1.jpg')

# john._pic = tig['public_id']
# sally._pic = tig['public_id']

john._pic = 'invtn6zt9ipi1fbtighn'
sally._pic = 'invtn6zt9ipi1fbtighn'
db.session.commit()
jessie = User.query.get('jjf4')
public = Group('Public', None, [jessie])
content = "UGH DEBUGGIN"
anotherpost = Post(content, jessie, [public])



add_friend_local('jexample', 'sstudent')


add_tag('jexample', "tag1")
search_tag("tag1")


db.session.add(public)
db.session.add(anotherpost)
db.session.commit()

user = User.query.get('jjf4')
feed = user.get_feed()
for post in feed:
    print(post.content)
# picurl, _ = cloudinary.utils.cloudinary_url(john._pic, width = 100, height = 150, crop = "fill")
# print(picurl)
