from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User, Tag
from orangepages.views.util import render


page = Blueprint('testsearch', __name__)



@page.route('/search')
def search_user():
    query_list = request.args.get('query').split(' ')

    # FIXME sry - zx
    if len(query_list) > 0 and len(query_list[0]) > 0 and query_list[0][0]=='#':
        tagged_posts = []

        for query in query_list:
            if query[0] == '#':
                print("hash", query[1:])
                posts = search_tag(query[1:])
                tagged_posts.extend(posts)

        return render('test/all_posts.html', posts=tagged_posts)

    user_preview_list = User.search(*query_list).all()
    query = ' '.join(query_list)

    return render('search.html',
    user_preview_list=user_preview_list, query=query, count=len(user_preview_list))

# helper method
def search_tag(tag_str):
    tag = Tag.query.get(tag_str)
    if tag == None:
        posts = []
    else:
        posts = tag.get_posts()
    return posts

# @page.route('/searchbar-tag')
# def searchbar_tag():
#     return render('test/searchbar-tag.html')
