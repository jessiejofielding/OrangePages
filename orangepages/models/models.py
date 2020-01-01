import datetime

from flask import Flask
from sqlalchemy import and_, create_engine, desc, asc, or_, PrimaryKeyConstraint
from sqlalchemy.orm import backref, relationship
from collections import defaultdict

import config
import flask_sqlalchemy as fsq
import orangepages.models.statuses as st
from orangepages import app, admin
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from urllib2 import urlopen
import requests

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db = fsq.SQLAlchemy(app)

DEF_IMG = 'https://res.cloudinary.com/hcfgcbhqf/image/upload/c_fill,h_120,w_120,g_face,r_10/r3luksdmal8hwkvzfc25.png'

def url_exists(url):
    request = requests.get(url)
    return request.status_code == 200

#-----------------------------------------------------------------------
class User(db.Model):
    """ User table """
    uid = db.Column(db.String(20), primary_key=True)
    _uid = db.Column(db.Integer, default=1)
    firstname = db.Column(db.String(50))
    _firstname = db.Column(db.Integer, default=1)
    lastname = db.Column(db.String(50))
    _lastname = db.Column(db.Integer, default=1)
    email = db.Column(db.String(50))
    _email = db.Column(db.Integer, default=1)

    hometown = db.Column(db.String(50))
    _hometown = db.Column(db.Integer, default=1)
    state = db.Column(db.String(50))
    _state = db.Column(db.Integer, default=1)
    country = db.Column(db.String(50))
    _country = db.Column(db.Integer, default=1)

    year = db.Column(db.String(50))
    _year = db.Column(db.Integer, default=1)
    major = db.Column(db.String(50))
    _major = db.Column(db.Integer, default=1)
    rescollege = db.Column(db.String(50))
    _rescollege = db.Column(db.Integer, default=1)
    school = db.Column(db.String(50))
    _school = db.Column(db.Integer, default=1)
    room = db.Column(db.String(50))
    _room = db.Column(db.Integer, default=1)
    building = db.Column(db.String(50))
    _building = db.Column(db.Integer, default=1)

    food = db.Column(db.String(50))
    _food = db.Column(db.Integer, default=1)
    team = db.Column(db.String(50))
    _team = db.Column(db.Integer, default=1)
    activities = db.Column(db.String(100))
    _activities = db.Column(db.Integer, default=1)
    certificate = db.Column(db.String(100))
    _certificate = db.Column(db.Integer, default=1)
    birthday = db.Column(db.String(50))
    _birthday = db.Column(db.Integer, default=1)

    _unread_notifs = db.Column(db.Integer, default=0)

    _dateofreg = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    _posts_made = relationship('Post', back_populates='creator')
    _groups = relationship('Group', back_populates='owner')
    _pic = db.Column(db.String(50), default='r3luksdmal8hwkvzfc25')

    _img = db.Column(db.Boolean(), default = False)

    def __init__(self, netid):
        self.uid = netid
        # every user is a member of the group public
        public = Group.query.get(1)
        public.add_member(self)

        friends = Group(netid + "'s friends", self, [])
        self._groups.append(friends)

        # For 'Just Me' privacy uhhh
        self._groups.append(Group(netid, self, [self]))
        db.session.add(self)
        db.session.commit()

    # TO REMOVE
    def update_pic(self, image):
        subpath = self.uid + "_pic.jpeg"
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], subpath))

    def add_img(self, image):
        if image is not None:
            self._img = True
            tig = cloudinary.uploader.upload(image)
            self._pic = tig['public_id']
            db.session.commit()


    def get_img(self):
        if self._img:
            x = cloudinary.CloudinaryImage(self._pic).url

            return x
        else:
            return DEF_IMG



    def update_public_info(self, firstname, lastname, email, rescollege, school,
    major, year):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.rescollege = rescollege
        self.school = school
        self.major = major
        self.year = year
        db.session.commit()


    def update_optional_info(self, hometown, state, country, room, building, food,
    team, activities, certificate, birthday, affiliations):
        self.hometown = hometown
        self.state = state
        self.country = country
        self.room = room
        self.building = building
        self.food = food
        self.team = team
        self.activities = activities
        self.certificate = certificate
        self.birthday = birthday
        for affil in affiliations:
            pass
        db.session.commit()

    # ###### TEMPORARY
    # defining this to match our current profile page's fields just to get it functioning
    ##### FIX fic xxi fix
    def update_profile_info(self, firstname,lastname,email,year,major,hometown,state,country,room,building):
        self.firstname, self.lastname, self.email,self.year,self.major,self.hometown,\
        self.state,self.country,self.room,self.building = \
            (firstname,lastname,email,year,major,hometown,state,country,room,building)
        db.session.commit()

    # helpers ---------------------------------------------------------
    # all attribute privacies as a list of gids
    def get_attr_priv(self):
        return (self._uid, self._firstname, self._lastname, self._email,
            self._hometown, self._state, self._country, self._year,
            self._major, self._rescollege, self._school, self._room,
            self._building, self._food, self._team, self._activities,
            self._certificate, self._birthday)

    # return list of privacy strings as list of corr. group ids
    def priv_to_group(self, privs):
        mapping = {
            'Public': 1,
            'Friends': self._groups[0].gid,
            'Just me': self._groups[1].gid,
        }
        groups = []
        for priv in privs:
            groups.append(mapping[priv])
        return groups

    # return list of gids as list of corr privacy strings
    def group_to_priv(self, groups):
        mapping = {
            1: 'Public',
            self._groups[0].gid: 'Friends',
            self._groups[1].gid: 'Just me'
        }
        privs = []
        for group in groups:
            privs.append(mapping[group])
        return privs

    # -----------------------------------------------------------------

    def update_privacy(self, uid, first, last, email, hometown, state,
        country, year, major, rescollege, school, room, building, food,
        team, activities, certificate, birthday):

        # print('\n\n update priv raw params:\n')
        # for i in (uid, first, last, email, hometown,
        #             state, country, year, major, rescollege, school, room,
        #             building, food, team, activities, certificate, birthday):
        #     print(i+ ' ')
        # print('\n\n')

        self._uid, self._firstname, self._lastname, self._email, \
        self._hometown, self._state, self._country, self._year, \
        self._major, self._rescollege, self._school, self._room, \
        self._building, self._food, self._team, self._activities, \
        self._certificate, self._birthday = \
        self.priv_to_group((uid, first, last, email, hometown,
            state, country, year, major, rescollege, school, room,
            building, food, team, activities, certificate, birthday))




        # print('\n\n update priv after params:\n')
        # for i in self.get_attr_priv():
        #     print(i)
        # print('\n\n')


        db.session.commit()

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

    # returns a map of the lookup_user's attributes, with consideration
    # of their privacy settings
    def lookup_user(self, uid):
        lookup_user = User.query.get(uid)

        names = ['netid', 'firstname', 'lastname', 'email', 'hometown',
            'state', 'country', 'year', 'major', 'rescollege', 'school',
            'room', 'building', 'food', 'team', 'activities', 'certificate',
            'birthday']

        vals = [lookup_user.uid, lookup_user.firstname, lookup_user.lastname, lookup_user.email,
            lookup_user.hometown, lookup_user.state, lookup_user.country, lookup_user.year,
            lookup_user.major, lookup_user.rescollege, lookup_user.school, lookup_user.room,
            lookup_user.building, lookup_user.food, lookup_user.team, lookup_user.activities,
            lookup_user.certificate, lookup_user.birthday]

        privs = lookup_user.get_attr_priv() # gid allowed to view each attr

        lookup = {}
        for name, priv, val in zip(names, privs, vals):
            if Group.query.get(priv) in self.groups_in.all():
                lookup[name] = val
            else:
                lookup[name] = ""
            # print(name + " " + str(lookup[name]))

        return lookup

    # Returns a list of users who have any visible attritute that matches
    # the given arguments. Any number of arguments can be given.
    def search(self, *args):
        attributes = []
        privacy = {}

        for x in User.__table__.columns:
            # to keep
            if str(x)[5] != "_":
                # TODO: this is where we could look at privacy settings with
                # a little work; we would need to take searcherid or searcher
                # (user object) as the first argument -jf
                attributes.append(x)
            else:
                name = str(x)[6:]
                privacy[name] = x

        group_ids = []
        for group in self.groups_in:
            group_ids.append(group.gid)
        users = db.session.query(User).\
            filter(and_(or_(and_(x.ilike('%' + val + '%'), or_(privacy[str(x)[5:]] == g for g in group_ids)) for x in attributes) for val in args))
        # or_(privacy[str(x)[5:]] == g for g in group_ids)
        return users

    def get_feed(self):
        p = db.session.query(Post)
        p = p.join(Post.groups)
        p = p.join(Group.members)
        p = p.filter(User.uid == self.uid)
        posts = p.order_by(desc(Post.date)).all()
        return posts

    # get all new posts since time
    def feed_new(self, time):
        p = db.session.query(Post).join(Post.groups).join(Group.members).filter(User.uid == self.uid)
        p = p.filter(Post.date > time)
        posts = p.order_by(desc(Post.date)).all()
        return posts

    # get next k posts after time
    def feed_next(self, time, k=10):
        p = db.session.query(Post).join(Post.groups).join(Group.members).filter(User.uid == self.uid)
        p = p.filter(Post.date < time)
        posts = p.order_by(desc(Post.date)).all()
        if len(posts) < k:
            return posts
        return posts[0:k]

    # get all posts within time range
    def feed_range(self, t_start, t_end):
        p = db.session.query(Post).join(Post.groups).join(Group.members).filter(User.uid == self.uid)
        p = p.filter(Post.date <= t_start)
        p = p.filter(Post.date >= t_end)
        posts = p.order_by(desc(Post.date)).all()
        return posts



    def liked_post(self, post_id):
        likedPost = self.posts_liked.filter(Post.pid == post_id).all()
        return len(likedPost) == 1

    # FRIENDS
    def add_friend(self, friend):
        if not self.is_friend(friend):
            self._groups[0].members.append(friend)
            friend._groups[0].members.append(self)

            db.session.commit()

    def unfriend(self, friend):
        if self.is_friend(friend):
            self._groups[0].members.remove(friend)
            friend._groups[0].members.remove(self)

            db.session.commit()

    def friend_list(self):
        # print(self._groups[0].members)
        return self._groups[0].members

    # ???
    def post_list(self):
        # print(self._groups[0].members)
        return self._posts_made

    # is user a friend of self?
    def is_friend(self, user):
        # is_friend = (user in self.friend_list())
        # return is_friend
        rel = Relationship.get_status(self, user)
        return rel == st.friends

    # has self sent a friend request to user?
    def friend_requested(self, user):

        rel = Relationship.get_status(self, user)
        user1 = self
        user2 = user

        if user1.uid < user2.uid:
            return rel == st.request1_2

        elif user2.uid < user1.uid:
            return rel == st.request2_1

        return False




#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------
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
        db.session.add(self)
        db.session.commit()

#-----------------------------------------------------------------------
class Relationship(db.Model):
    """ Relationship table """
    user1id = db.Column(db.String(20), db.ForeignKey('user.uid'))
    user1 = relationship('User',
                        foreign_keys=[user1id])
    user2id = db.Column(db.String(20), db.ForeignKey('user.uid'))
    user2 = relationship('User',
                        foreign_keys=[user2id])
    status = db.Column(db.String(50))
    __table_args__ = (
        PrimaryKeyConstraint('user1id', 'user2id'),
        {},
    )

    def __init__(self, user1, user2, status):
        assert(user1.uid < user2.uid)
        self.user1 = user1
        self.user2 = user2
        self.status = st.none
        self.change_status(status)
        db.session.add(self)
        db.session.commit()


    def change_status(self, status):
        # print('status', type(status), 'st.unfriend', type(st.unfriend))
        if ((status == st.request2_1) and (self.status == st.request1_2)) or \
            ((status == st.request1_2) and (self.status == st.request2_1)):
            status = st.friends

        if status == st.accept:
            status = st.friends

        if (status == st.friends) and (int(self.status) != st.friends):
            self.user1.add_friend(self.user2)

        if (status == st.unfriend) and (int(self.status) == st.friends):
            self.user1.unfriend(self.user2)

        self.status = status
        db.session.commit()


    def get_status(user1, user2):

        if user1.uid < user2.uid:
            try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user1.uid), Relationship.user2.has(uid=user2.uid))).all()[0]
            except:
                return -1

        elif user2.uid < user1.uid:
            try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user2.uid), Relationship.user2.has(uid=user1.uid))).all()[0]
            except:
                return -1

        elif user1.uid == user2.uid:
            return 0

        return int(rel.status)


#-----------------------------------------------------------------------
class Comment(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.pid'))
    content = db.Column(db.String(1000))
    creatorid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    # creator = db.Column(db.String(20), db.ForeignKey('user.uid'))
    creator = relationship('User', backref=backref('_comments_posted', lazy='dynamic'),
        foreign_keys=[creatorid])
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    post = relationship('Post', backref=
        backref('comments', lazy='dynamic'))

    def __init__(self, postid, content, creator):
        self.postid = postid
        self.content = content
        self.creator = creator
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "Comment %s by %s" % (self.content, self.creator)


#-----------------------------------------------------------------------
class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000))
    creatorid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    creator = relationship('User', back_populates='_posts_made')
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    has_img = db.Column(db.Boolean(), default=False)
    _pic = db.Column(db.String(50))
    last_edited = db.Column(db.DateTime)

    likes = relationship('User', secondary=post_liker,
                            backref=backref('posts_liked', lazy='dynamic'))

    groups = relationship('Group', secondary=post_group,
                            backref=backref('posts', lazy='dynamic'))

    # TODO: tags
    tags = relationship('Tag', secondary=post_tag,
                        backref=backref('posts', lazy='dynamic'))

    def add_group(self, group):
        if group not in self.groups: self.groups.append(group)

    def remove_group(self, group):
        if group in self.groups: self.groups.remove(group)

    def get_visibility(self):
        if Group.query.get(1) in self.groups:
            return "Everyone can see this"
        elif self.creator._groups[0] in self.groups:
            return "Only your friends can see this"
        else:
            return "Only you can see this"

        # vis_str = "Visible to: "
        # for group in self.groups:
        #     if group == self.creator._groups[0]:
        #         vis_str += "your friends" + ", "
        #     elif group == self.creator._groups[1]:
        #         vis_str += "yourself" + ", "
        #     else:
        #         vis_str += group.title + ", "
        # vis_str = vis_str[:-1]
        # return vis_str

    # 'Friends' or 'Public'; visibility is a string sorry
    def set_visibility(self, visibility):
        if visibility == 'Public':
            self.add_group(Group.query.get(1))
        elif visibility == 'Friends':
            self.remove_group(Group.query.get(1))
            self.add_group(self.creator._groups[0]) # friends group
        elif visibility == 'Just me':
            self.remove_group(Group.query.get(1))
            self.remove_group(self.creator._groups[0])

        self.add_group(self.creator._groups[1]) # just me group

    def add_tag(self, tag):
        if tag not in self.tags: self.tags.append(tag)

    def add_tag_str(self, tag_str):
        tag = Tag.query.get(tag_str)
        if tag is None:
            tag = Tag(tag_str)

        if tag not in self.tags: self.tags.append(tag)

    def get_tags(self):
        return self.tags

    def remove_tag(self, tag):
        if tag not in self.tags:
            print("Post did not have this tag")
        else:
            self.tags.remove(tag)

    def update_last_edit(self):
        self.last_edited = datetime.datetime.utcnow()
        db.session.commit()

    def add_like(self, liker):
        # print(liker.firstname, "liked post", self.pid)
        self.likes.append(liker)

    def unlike(self, unliker):
        if unliker not in self.likes:
            print("User %s did not like this post" % unliker.uid)
        else:
            self.likes.remove(unliker)
            notifs = db.session.query(Notification).filter(
                (Notification.action == NType.LIKED),
                (Notification.targetid == self.creator.uid),
                (Notification.senderid == unliker.uid),
                (Notification.postid == self.pid)
                )
            for notif in notifs.all():
                notif.delete()

    def get_likers(self):
        return self.likes

    def get_comments(self):
        c = self.comments
        comments = c.order_by(desc(Comment.date)).all()
        return comments

    def prev_comments(self):
        c = self.comments.order_by(asc(Comment.date)).all()
        if len(c) < 3:
            return c
        return c[-3:]

    def num_comments(self):
        return len(self.comments.all())

    def add_img(self, image):
        if image is not None:
            self.has_img = True
            tig = cloudinary.uploader.upload(image)
            self._pic = tig['public_id']
            db.session.commit()

    def get_img(self):
        if self.has_img:
            x = cloudinary.CloudinaryImage(self._pic).url
            return x
        else:
            return ""

    def del_img(self):
        if self.has_img:
            self.img = ""
            self.has_img = False

    def update_info(self, content, groups=[], tags=[]):
        self.content = content

        for group in groups:
            self.add_group(group)

        # remove old tags
        self.tags = []

        for tag_str in tags:
            self.add_tag_str(tag_str)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Post %s by %s" % (self.content, self.creator)

    def __init__(self, creator):
        self.creator = creator
        self.img = ""
        # self.update_info(content, groups, tags)
        db.session.add(self)
        db.session.commit()


#-----------------------------------------------------------------------
class Tag(db.Model):
    tid = db.Column(db.String(1000), primary_key=True)
    # db.Column(db.Integer, primary_key=True, autoincrement=True)
    # tag = db.Column(db.String(1000))
    # use tag.posts to get all the posts with this tag

    def __init__(self, tag):
        self.tid = tag
        # db.session.add(self) REVIEW do we need this

    def __repr__(self):
        return "<Tag: %s>" % (self.tid)

    def get_posts(self, user):
        p = self.posts
        p = p.join(Post.groups)
        p = p.join(Group.members)
        p = p.filter(User.uid == user.uid)
        posts = p.order_by(desc(Post.date)).all()
        return posts

# only works after db initialised
# Returns the public group that every user is automatically part of
def public_group():
    public = Group.query.get(1)
    return public

#-----------------------------------------------------------------------
class NType:
    # Notification type
    LIKED, COMMENTED, REQUESTED, ACCEPTED, TAGGED = range(5)
    text = {
            LIKED: 'liked your post.',
            COMMENTED: 'commented on your post.',
            REQUESTED: 'sent you a friend request.',
            ACCEPTED: 'accepted your friend request.',
            TAGGED: 'tagged you in a post.'
        }

class Notification(db.Model):

    nid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.Integer)
    text = db.Column(db.String(500))
    unread = db.Column(db.Boolean, default=True)

    # target: person who receives this notification.
    # sender: person who triggered the notification.

    targetid = db.Column(db.String(20), db.ForeignKey('user.uid'))
    senderid = db.Column(db.String(20), db.ForeignKey('user.uid'))

    target = relationship('User', backref=backref('notifs',
        order_by='desc(Notification.date)', lazy='dynamic'),
        foreign_keys=[targetid])
    sender = relationship('User', backref=backref('_notifs_sent', lazy='dynamic'),
        foreign_keys=[senderid])

    # Optional
    postid = db.Column(db.Integer)




    def __init__(self, sender, target, action, post=None):
        self.target = target
        self.sender = sender
        self.action = action
        if self.target._unread_notifs < 0:
                self.target._unread_notifs = 1
        else:
            self.target._unread_notifs += 1

        if post is not None:
            self.postid = post.pid

        self.text = NType.text[action]

        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        string = "To %s: %s %s\n"
        return string  % (self.targetid, self.senderid, self.text)

    def sender_name(self):
        return self.sender.firstname + ' ' + self.sender.lastname

    def sender_id(self):
        return self.sender.uid

    def link_to(self):
        if self.action in (NType.LIKED, NType.COMMENTED, NType.TAGGED):
            return '/post/' + str(self.postid)
        else:
            return '/profile/' + self.sender.uid

    def mark_read(self):
        if self.unread:
            self.unread = False
            if self.target._unread_notifs < 0:
                self.target._unread_notifs = 0
            else:
                self.target._unread_notifs -= 1
            db.session.commit()

    def delete(self):
        if self.unread:
            if self.target._unread_notifs < 0:
                self.target._unread_notifs = 0
            else:
                self.target._unread_notifs -= 1
        self.target.notifs.remove(self)
        self.sender._notifs_sent.remove(self)
        db.session.delete(self)
        db.session.commit()
