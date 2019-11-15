from flask import request, redirect, make_response
from flask import Blueprint, render_template
from orangepages.models.models import db, User, Group, Post, Comment
from orangepages.views.util import cur_user, cur_uid, render
# from flask_login import current_user, login_required


page = Blueprint('post', __name__)

@page.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method=='GET':
        return render('post_create.html')

    user = cur_user()
    content = request.form.get('content')

    # group with everyone in it
    public = Group.query.get(1)

    post = Post(content, user, [public])
    db.session.add(post)
    db.session.commit()

    return redirect("/feed")

@page.route('/post/<int:postid>', methods=['GET'])
def view_post(postid):
    post = Post.query.get(postid)
    comments = post.get_comments()
    return render("post.html", post=post, comments=comments)

@page.route('/post/<int:postid>/comment', methods=['GET', 'POST'])
def comment(postid):
    post = Post.query.get(postid)

    if request.method=='GET':
        return render("post_comment.html", post=post)
    else:
        user = cur_user()
        content = request.form.get('content')

        comment = Comment(postid, content, cur_uid())
        db.session.add(comment)
        db.session.commit()

        return redirect('/post/' + str(postid))

# @page.route('/post/<int:post_id>', methods=['GET'])
# def feed_post(post_id):
#     # # TODO:
#     return


@page.route('/post/<int:post_id>/like', methods=['POST'])
def like(post_id):
    # # TODO:
    return
