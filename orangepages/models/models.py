import flask_sqlalchemy as fsq
from flask import Flask
from sqlalchemy.orm import relationship, backref
import datetime
# from orangepages import app

# TODO: import app
app = Flask(__name__)

# engine = fsq.create_engine('sqlite:////Users/jessie/OrangePages/test.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jessie/OrangePages/test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = fsq.SQLAlchemy(app)

class User(db.Model):
    """ User table """
    uid = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, netid, firstname, lastname, email):
        self.uid = netid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

""" Secondary tables for many-to-many relationships. """
post_group = db.Table('post_group',
    db.Column('post_id', db.Integer, db.ForeignKey('post.pid')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.gid'))
)

post_liker = db.Table('post_liker', User.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.pid')),
    db.Column('user_id', db.String(20), db.ForeignKey('user.uid'))
)

group_member = db.Table('group_member', User.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('group.gid')),
    db.Column('user_id', db.String(20), db.ForeignKey('user.uid'))
)

class Group(db.Model):
    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    ownerid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    members = relationship('User', secondary=group_member,
                            backref=backref('groups_in', lazy='dynamic'))
    
    def add_member(self, member):
        # TODO: add entry to group_member table
        pass

    def remove_member(self, member):
        # TODO: remove entry from group_member table
        pass

    def __init__(self, title, ownerid, members):
        self.title = title
        self.ownerid = ownerid
        for member in members:
            self.add_member(member)

class Relationship(db.Model):
    """ Relationship table """
    user1 = db.Column(db.String(20), db.ForeignKey('user.uid'), primary_key=True)
    user2 = db.Column(db.String(20), db.ForeignKey('user.uid'), primary_key=True)
    status = db.Column(db.String(50))

    def __init__(self, user1, user2, status):
        assert(user1 < user2)
        self.user1 = user1
        self.user2 = user2
        self.status = status

class Comment(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.pid'))
    content = db.Column(db.String(1000))
    creator = db.Column(db.String(20), db.ForeignKey('user.uid'))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    post = relationship('Post', backref=
        backref('comments', lazy='dynamic'))

    def __init__(self, postid, content, creator):
        self.postid = postid
        self.content = content
        self.creator = creator


class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000))
    creatorid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    likes = relationship('User', secondary=post_liker,
                            backref=backref('posts_liked', lazy='dynamic'))

    groups = relationship('Group', secondary=post_group,
                            backref=backref('posts', lazy='dynamic'))

    # TODO: tags
    
    def add_group(self, group):
        # TODO: add entry to post_group table
        pass

    def add_like(self, liker):
        # TODO: add entry to post_liker table
        pass

    # TODO: remove groups and likes?

    def __init__(self, content, creatorid, groups):
        self.content = content
        self.creatorid = creatorid
        for group in groups:
            self.add_group(group)
    
