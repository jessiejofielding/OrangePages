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
    #query = request.args.get('query')

    user_preview_list = User.search("sa")
    print(user_preview_list)

    # return render_template('test-search.html', query=query,
    # user_preview_list=user_preview_list)
