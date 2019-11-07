from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User

page = Blueprint('testsearch', __name__)



@page.route('/search')
def search_user():
    query_list = request.args.get('query').split(' ')
    user_preview_list = User.search(*query_list).all()
    query = ' '.join(query_list)

    return render_template('search.html',
    user_preview_list=user_preview_list, query=query)

