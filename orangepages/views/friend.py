from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User
from flask_cas_fix import login_required
from sqlalchemy import exc

from orangepages.views.util import cur_user, cur_uid, render



page = Blueprint('friend', __name__)

@page.route('/profile/<string:lookup_id>/add-friend', methods=['POST'])
def add_friend(lookup_id):
    user1 = cur_user()
    user2 = User.query.get(lookup_id)
    user1.add_friend(user2)

@page.route('/profile/<string:lookup_id>/unfriend', methods=['POST'])
def unfriend(lookup_id):
    user1 = cur_user()
    user2 = User.query.get(lookup_id)
    user1.unfriend(user2)

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
