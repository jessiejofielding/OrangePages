import datetime

from flask import Flask
from sqlalchemy import and_, create_engine, desc, or_
from sqlalchemy.orm import backref, relationship

import config
import flask_sqlalchemy as fsq
import orangepages.models.statuses as st
from orangepages import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db = fsq.SQLAlchemy(app)

class User(db.Model):
    """ User table """
    uid = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    hometown = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    year = db.Column(db.String(50))
    major = db.Column(db.String(50))
    room = db.Column(db.String(50))
    building = db.Column(db.String(50))

    _dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)
    _posts_made = relationship('Post', back_populates='creator')
    _groups = relationship('Group', back_populates='owner')
    _pic = db.Column(db.String(50), default='r3luksdmal8hwkvzfc25')

    def __init__(self, netid, firstname, lastname, email):
        self.uid = netid
        self.update_info(firstname, lastname, email)
        # every user is a member of the group public
        public = Group.query.get(1)
        public.add_member(self)

        friends = Group(netid + "'s friends", self, [])
        self._groups.append(friends)

    def update_info(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def update_optional_info(self, firstname, lastname, email, hometown,
    state, country, year, major, room, building):
        self.update_info(firstname, lastname, email)
        self.hometown = hometown
        self.state = state
        self.country = country
        self.year = year
        self.major = major
        self.room = room
        self.building = building

    # for debugging
    # def __repr__(self):
    #     return "<User(uid='%s', firstname='%s', lastname='%s', email='%s')>" % (
    #     self.uid, self.firstname, self.lastname, self.email)

    # for debugging
    def __repr__(self):
        str = "<User(uid='%s', firstname='%s', lastname='%s', email='%s', " + \
        "hometown='%s', state='%s', country='%s', year='%s', " + \
        "major='%s', room='%s', building='%s')>"

        return str % (self.uid, self.firstname, self.lastname, self.email,
        self.hometown, self.state, self.country, self.year,
        self.major, self.room, self.building)

    # Returns a list of users who have any visible attritute that matches
    # the given arguments. Any number of arguments can be given.
    def search(*args):
        attributes = []
        for x in User.__table__.columns:
            # to keep
            if str(x)[5] != "_":
                # TODO: this is where we could look at privacy settings with
                # a little work; we would need to take searcherid or searcher
                # (user object) as the first argument -jf
                attributes.append(x)

        users = db.session.query(User).\
            filter(and_(or_(x.ilike('%' + val + '%') for x in attributes ) for val in args))

        return users

    def get_feed(self):
        p = db.session.query(Post)
        p = p.join(Post.groups)
        p = p.join(Group.members)
        p = p.filter(User.uid == self.uid)
        posts = p.order_by(desc(Post.date)).all()
        return posts

    def liked_post(self, post_id):
        likedPost = self.posts_liked.filter(Post.pid == post_id).all()
        return len(likedPost) == 1

    # FRIENDS
    def add_friend(self, friend):
        self._groups[0].members.append(friend)
        friend._groups[0].members.append(self)
        # print("after adding friend, friendlist of ", self.uid, " : ", self._groups[0].members)
        # print("after adding friend, friendlist of ", friend.uid, " : ", friend._groups[0].members)

    def unfriend(self, friend):
        if friend in self._groups[0].members:
            self._groups[0].members.remove(friend)
            friend._groups[0].members.remove(self)
            # print("after removing friend, friendlist of ", self.uid, " : ", self._groups[0].members)
            # print("after removing friend, friendlist of ", friend.uid, " : ", friend._groups[0].members)
        else:
            print(friend.uid, " not a friend of ", self.uid)

    def friend_list(self):
        return self._groups[0].members

    # is user a friend of self?
    def is_friend(self, user):
        is_friend = (user in self.friend_list())
        return is_friend

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

post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.pid')),
    db.Column('tag_id', db.String(20), db.ForeignKey('tag.tid'))
)

class Group(db.Model):
    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    ownerid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    owner = relationship('User', back_populates='_groups')
    members = relationship('User', secondary=group_member,
                            backref=backref('groups_in', lazy='dynamic'))

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    # TODO: may want to do a "is_member" method -jf

    def __init__(self, title, owner, members):
        self.title = title
        self.owner = owner
        for member in members:
            self.add_member(member)

class Relationship(db.Model):
    """ Relationship table """
    user1id = db.Column(db.String(20), db.ForeignKey('user.uid'), primary_key=True)
    user1 = relationship('User',
                        foreign_keys=[user1id])
    user2id = db.Column(db.String(20), db.ForeignKey('user.uid'), primary_key=True)
    user2 = relationship('User',
                        foreign_keys=[user2id])
    status = db.Column(db.String(50))

    def change_status(self, status):
        if ((status == st.request2_1) and (self.status == st.request1_2)) or \
            ((status == st.request1_2) and (self.status == st.request2_1)):
            status = st.friends

        if status == st.accept:
            status = st.friends

        if status == st.friends:
            # add to "Friend" group
            if self.status != st.friends:
                self.user1.add_friend(self.user2)
        self.status = status

    def __init__(self, user1, user2, status):
        assert(user1.uid < user2.uid)
        self.user1 = user1
        self.user2 = user2
        self.status = st.none
        self.change_status(status)

    def get_status(user1, user2):
        # TODO: finish implementing this - jf
        # if user1.uid > user2.uid:
        #     temp = user2
        #     user2 = user1
        #     user1 = temp
        # rel = Relationship.query.filter(user1=user1, user2=user2)
        # status = rel.status
        pass

class Comment(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.pid'))
    content = db.Column(db.String(1000))
    #creatorid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    creator = db.Column(db.String(20), db.ForeignKey('user.uid'))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    post = relationship('Post', backref=
        backref('comments', lazy='dynamic'))

    def __init__(self, postid, content, creator):
        self.postid = postid
        self.content = content
        self.creator = creator

    def __repr__(self):
        return "Comment %s by %s" % (self.content, self.creator)


class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000))
    creatorid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    creator = relationship('User', back_populates='_posts_made')
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    likes = relationship('User', secondary=post_liker,
                            backref=backref('posts_liked', lazy='dynamic'))

    groups = relationship('Group', secondary=post_group,
                            backref=backref('posts', lazy='dynamic'))

    # TODO: tags
    tags = relationship('Tag', secondary=post_tag,
                        backref=backref('posts', lazy='dynamic'))

    def add_group(self, group):
        if group not in self.groups: self.groups.append(group)

    def add_tag(self, tag):
        if tag not in self.tags: self.tags.append(tag)

    def get_tags(self):
        return self.tags

    def add_like(self, liker):
        print(liker.firstname, "liked post", self.pid)
        self.likes.append(liker)

    def remove_group(self, group):
        self.groups.remove(group)

    def remove_tag(self, tag):
        if tag not in self.tags:
            print("Post did not have this tag")
        else:
            self.tags.remove(tag)

    def unlike(self, unliker):
        if unliker not in self.likes:
            print("User %s did not like this post" % unliker.uid)
        else:
            self.likes.remove(unliker)

    def get_likers(self):
        return self.likes

    def get_comments(self):
        c = db.session.query(Comment)
        c = c.filter(Comment.postid == self.pid)
        comments = c.order_by(desc(Comment.date)).all()
        return comments

    def __repr__(self):
        return "Post %s by %s" % (self.content, self.creator)

    def __init__(self, content, creator, groups):
        self.content = content
        self.creator = creator
        for group in groups:
            self.add_group(group)


class Tag(db.Model):
    tid = db.Column(db.String(1000), primary_key=True)
    # db.Column(db.Integer, primary_key=True, autoincrement=True)
    # tag = db.Column(db.String(1000))
    # use tag.posts to get all the posts with this tag

    def __init__(self, tag):
        self.tid = tag

    def __repr__(self):
        return "<Tag: %s>" % (self.tid)

    def get_posts(self):
        posts = self.posts.all()
        return posts
