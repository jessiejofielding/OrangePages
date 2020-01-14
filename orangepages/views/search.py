from flask import request, make_response, jsonify
from flask import Blueprint, render_template
from orangepages.models.models import User, Tag
from orangepages.views.util import render, cur_user, user_required
import re


page = Blueprint('testsearch', __name__)

@page.route('/search')
@user_required
def search_user():
    query = request.args.get('query')
    pattern = re.compile(r'\"(.+?)\"$')
    match = pattern.match(query)
    
    if match is not None:
        query_list = [query[1:-1]]
        exact = True
    else:
        query_list = request.args.get('query').split(' ')
        exact = False


    posts = search_tag(query_list)
    user_preview_list = cur_user().search(*query_list, exact=exact).all()
    query = ' '.join(query_list)

    return render('search.html', posts=posts,
    user_preview_list=user_preview_list, query=query, exact=exact)

# helper method
def search_tag(query_list):
    tagged_posts = []
    for query in query_list:
        print("hash", query)

        tags = Tag.query.filter_by(tid=query).all()
        if len(tags) == 0:
            posts = []
        else:
            for tag in tags:
                posts = tag.get_posts(cur_user())

        tagged_posts.extend(posts)

    return tagged_posts

@page.route('/autocomplete', methods=['GET'])
def autocomplete():
    query_list = request.args.get('query').split(' ')
    users = cur_user().search(*query_list, exact=False).all()
    results = [{'label':user.firstname + " " + user.lastname, 'value':user.uid} for user in users]
    return jsonify(results=results)

# @page.route('/searchbar-tag')
# def searchbar_tag():
#     return render('test/searchbar-tag.html')
