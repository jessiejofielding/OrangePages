from sqlalchemy import create_engine, or_
import flask_sqlalchemy as fsq
from flask import Flask
from sqlalchemy.orm import relationship, backref, sessionmaker
import datetime
import config
# from orangepages import app

# TODO: import app
app = Flask(__name__)

# configurations - #TODO: move somewhere permanent
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session = sessionmaker(bind=engine)

db = fsq.SQLAlchemy(app)

class User(db.Model):
    """ User table """
    uid = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)
    posts_made = relationship('Post', back_populates='creator')
    groups = relationship('Group', back_populates='owner')

    def __init__(self, netid, firstname, lastname, email):
        self.uid = netid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

        # for debugging
    def __repr__(self):
        return "<User(uid='%s', firstname='%s', lastname='%s', email='%s')>" % (
        self.uid, self.firstname, self.lastname, self.email)

        # Returns a list of users whose first or last names match
        # any of the given arguments. Any number of arguments can be given.
    def search(*args):
        session = Session()

        user_list = []

        for val in args:
            for user in session.query(User).\
            filter(or_(User.firstname.ilike('%' + val + '%'), User.lastname.ilike('%' + val + '%'))):
                user_list.append(user)

        return user_list

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
    owner = relationship('User', back_populates='groups')
    members = relationship('User', secondary=group_member,
                            backref=backref('groups_in', lazy='dynamic'))

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def __init__(self, title, owner, members):
        self.title = title
        self.owner = owner
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
    creator = relationship('User', back_populates='posts_made')
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    likes = relationship('User', secondary=post_liker,
                            backref=backref('posts_liked', lazy='dynamic'))

    groups = relationship('Group', secondary=post_group,
                            backref=backref('posts', lazy='dynamic'))

    # TODO: tags

    def add_group(self, group):
        self.groups.append(group)

    def add_like(self, liker):
        self.likes.append(liker)

    def remove_group(self, group):
        self.groups.remove(group)

    def unlike(self, unliker):
        self.likes.remove(unliker)

    def __init__(self, content, creator, groups):
        self.content = content
        self.creator = creator
        for group in groups:
            self.add_group(group)
