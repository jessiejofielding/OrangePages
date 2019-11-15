from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User
from orangepages.views.util import render


page = Blueprint('testsearch', __name__)



@page.route('/search')
def search_user():
    query_list = request.args.get('query').split(' ')
    user_preview_list = User.search(*query_list).all()
    query = ' '.join(query_list)

    return render('search.html',
    user_preview_list=user_preview_list, query=query, count=len(user_preview_list))

