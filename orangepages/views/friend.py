from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User, NType, Notification, Relationship
from flask_cas_fix import login_required
from sqlalchemy import exc, and_

from orangepages.views.util import cur_user, cur_uid, render, user_required
import orangepages.models.statuses as st


page = Blueprint('friend', __name__)


@page.route('/profile/friend-request', methods=['POST'])
@user_required
def friend_request():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)

    if user1.uid < user2.uid:
        status = st.request1_2
        try:
            rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user1.uid), Relationship.user2.has(uid=user2.uid))).all()[0]
        except:
            rel = Relationship(user1, user2, status)
        rel.change_status(status)

    if user2.uid < user1.uid:
        status = st.request2_1
        try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user2.uid), Relationship.user2.has(uid=user1.uid))).all()[0]
        except:
            rel = Relationship(user2, user1, status)
        rel.change_status(status)

    notif = Notification(user1, user2, NType.REQUESTED)

    return redirect(request.referrer)



@page.route('/profile/add-friend', methods=['POST'])
@user_required
def add_friend():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)
    # user1.add_friend(user2)

    status = st.friends

    if user1.uid < user2.uid:
        try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user1.uid), Relationship.user2.has(uid=user2.uid))).all()[0]
        except:
            rel = Relationship(user1, user2, status)
        rel.change_status(status)

    if user2.uid < user1.uid:
        try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user2.uid), Relationship.user2.has(uid=user1.uid))).all()[0]
        except:
            rel = Relationship(user2, user1, status)
        rel.change_status(status)

    notif = Notification(user1, user2, NType.ACCEPTED)

    return redirect(request.referrer)

@page.route('/profile/unfriend', methods=['POST'])
@user_required
def unfriend():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)
    # user1.unfriend(user2)
    status = st.unfriend

    if user1.uid < user2.uid:
        try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user1.uid), Relationship.user2.has(uid=user2.uid))).all()[0]
        except:
            rel = Relationship(user1, user2, status)
        rel.change_status(status)

    if user2.uid < user1.uid:
        try: rel = Relationship.query.filter(and_(Relationship.user1.has(uid=user2.uid), Relationship.user2.has(uid=user1.uid))).all()[0]
        except:
            rel = Relationship(user2, user1, status)
        rel.change_status(status)

    return redirect(request.referrer)

# @page.route('/friends-list', methods=['GET'])
# def friends_list():
#     user = cur_user()
#     friend_list = user.friend_list()
#     return render('friends.html',
#     friend_list = friend_list, lookup_user=user)

@page.route('/profile/<string:lookup_id>/friends-list', methods=['GET'])
@user_required
def friends_list(lookup_id):
    user = User.query.get(lookup_id)
    if user is None:
        return render('message.html',
            title='Error',
            message="This user doesn't exist.")


    friend_list = user.friend_list()
    return render('friends.html',
    friend_list = friend_list, lookup_user=user)

# @page.route('/profile/<string:lookup_id>/are-friends', methods=['GET'])
# def are_friends(lookup_id):
#     user2 = User.query.get(lookup_id)
#     are_friends = (user2 in cur_user().friend_list())
