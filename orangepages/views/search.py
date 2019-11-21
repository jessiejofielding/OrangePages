from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User, Tag
from orangepages.views.util import render


page = Blueprint('testsearch', __name__)



@page.route('/search')
def search_user():
    query_list = request.args.get('query').split(' ')

    # print("len(query_list)", len(query_list))
    if len(query_list) > 0 and len(query_list[0]) > 0:
        if query_list[0][0] == '#':
            print("hash", query_list[0][1:])
            posts = search_tag(query_list[0][1:])
            return render('test/all_posts.html', posts=posts)

    user_preview_list = User.search(*query_list).all()
    query = ' '.join(query_list)

    return render('search.html',
    user_preview_list=user_preview_list, query=query, count=len(user_preview_list))

# @page.route('/search-tag')
# helper method
def search_tag(tag_str):
    # tag_str = request.form.get('content')
    tag = Tag.query.get(tag_str)
    if tag == None:
        posts = []
    else:
        posts = tag.get_posts()
    return posts

# @page.route('/searchbar-tag')
# def searchbar_tag():
#     return render('test/searchbar-tag.html')
