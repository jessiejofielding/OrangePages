# For testing with templates/test-*.html

from flask import request, make_response, url_for
from flask import Blueprint, render_template
from orangepages.models.models import User

page = Blueprint('test', __name__)

#-----------------------------------------------------------------------
# search.py

@page.route('/test-page')
def testpage():
    return render_template('test-page.html')

@page.route('/test-search')
def testsearch():
    query = request.args.get('query')

    query_list = query.split()
    user_preview_list = User.search(*query_list)

    return render_template('test-search.html', query=query,
    user_preview_list=user_preview_list)

def testsearch_local(query):
    query_list = query.split()
    user_preview_list = User.search(*query_list)
    for user in user_preview_list:
        print(user)

# app name 
@page.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
# defining function 
  return render_template("404.html") 
#-----------------------------------------------------------------------
# general.py

# TEMPORARY: user in url bc we dont have login/cookies yet
@page.route('/test-feed/<string:lookup_id>', methods=['GET'])
# @login_required
def test_feed(lookup_id):
    # # TODO:
    user = User.query.get(lookup_id)
    return render_template('test-feed.html', posts=user.get_feed())

#-----------------------------------------------------------------------
# user.py

@page.route('/test-profile/<string:lookup_id>', methods=['GET'])
def test_view_profile(lookup_id):
    user = User.query.get(lookup_id)
    return render_template('test-profile.html', user=user)

# @page.route('/create-user', methods=['POST'])
# def test_create_user():
#     # # TODO:
#     User(netid, firstname, lastname, email)
#     return

# @page.route('/edit-user', methods=['PUT'])
# def test_edit_user():
#     # # TODO:
#     user.update_info(firstname, lastname, email)
#     return
