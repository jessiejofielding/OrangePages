from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User
from flask_cas_fix import login_required
from sqlalchemy import exc

from orangepages.views.util import cur_user, cur_uid, render



page = Blueprint('friend', __name__)

@page.route('/test/add-friend', methods=['GET'])
def view_add_friend():
    # friend_uid = 'zkoh'
    return render('/test/friend_add.html')

@page.route('/profile/add-friend', methods=['POST'])
def add_friend():
    user1 = cur_user()
    friend_uid = request.form.get('content')
    user2 = User.query.get(friend_uid)
    user1.add_friend(user2)
    return redirect(request.referrer)

@page.route('/profile/<string:lookup_id>/unfriend', methods=['POST'])
def unfriend(lookup_id):
    print("lookup_id", lookup_id)
    user1 = cur_user()
    user2 = User.query.get(lookup_id)
    user1.unfriend(user2)
    return redirect(request.referrer)

@page.route('/friends-list', methods=['GET'])
def friends_list():
    user = cur_user()
    friend_list = user.friend_list()
    return render('/test/friend_list.html',
    friend_list = friend_list)

# @page.route('/profile/<string:lookup_id>/are-friends', methods=['GET'])
# def are_friends(lookup_id):
#     user2 = User.query.get(lookup_id)
#     are_friends = (user2 in cur_user().friend_list())
