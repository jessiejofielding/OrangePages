from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User, NType, Notification
from flask_cas_fix import login_required
from sqlalchemy import exc

from orangepages.views.util import cur_user, cur_uid, render



page = Blueprint('friend', __name__)


@page.route('/profile/friend-request', methods=['POST'])
def friend_request():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)

    notif = Notification(user1, user2, NType.REQUESTED)
    db.session.add(notif)
    db.session.commit()
    
    return redirect(request.referrer)



@page.route('/profile/add-friend', methods=['POST'])
def add_friend():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)
    user1.add_friend(user2)

    notif = Notification(user1, user2, NType.ACCEPTED)
    db.session.add(notif)
    db.session.commit()

    return redirect(request.referrer)

@page.route('/profile/unfriend', methods=['POST'])
def unfriend():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)
    user1.unfriend(user2)
    return redirect(request.referrer)

# @page.route('/friends-list', methods=['GET'])
# def friends_list():
#     user = cur_user()
#     friend_list = user.friend_list()
#     return render('friends.html',
#     friend_list = friend_list, lookup_user=user)

@page.route('/profile/<string:lookup_id>/friends-list', methods=['GET'])
def friends_list(lookup_id):
    user = User.query.get(lookup_id)
    friend_list = user.friend_list()
    return render('friends.html',
    friend_list = friend_list, lookup_user=user)

# @page.route('/profile/<string:lookup_id>/are-friends', methods=['GET'])
# def are_friends(lookup_id):
#     user2 = User.query.get(lookup_id)
#     are_friends = (user2 in cur_user().friend_list())
