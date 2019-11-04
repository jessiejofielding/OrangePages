from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User

page = Blueprint('testsearch', __name__)


@page.route('/test-page')
def testpage():
    # # TODO:
    return render_template('test-page.html')

@page.route('/test-search')
def testsearch():
    query = request.args.get('query')

    query_list = query.split()
    user_preview_list = User.search(*query_list)

    return render_template('user-previews.html',
    user_preview_list=user_preview_list)

def testsearch_local(query):
    query_list = query.split()
    user_preview_list = User.search(*query_list)
    for user in user_preview_list:
        print(user)
