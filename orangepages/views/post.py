from flask import request, redirect, make_response
from flask import Blueprint, render_template, send_from_directory
from orangepages.models.models import db, User, Group, Post, Comment, Tag, NType, Notification
from orangepages.views.util import cur_user, cur_uid, render, user_required
from orangepages import app
import os
# from flask_login import current_user, login_required


page = Blueprint('post_page', __name__)


@page.route('/create-post', methods=['POST', 'GET'])
@user_required
def create_post():
    if request.method=='GET':
        return render('post_create.html')

    user = cur_user()
    post = Post(user)

    edit_post_util(post, request)

    return redirect("/feed")

@page.route('/post/<int:postid>/edit', methods=['POST', 'GET'])
def edit_post(postid):
    post = Post.query.get(postid)

    if request.method=='GET':
        return render('post_edit.html', post=post)

    edit_post_util(post, request)

    return redirect("/feed")

def edit_post_util(post, request):
    user = cur_user()
    content = request.form.get('content')

    # TAGS Parse tags and add them - list of tag STRINGS
    tags = []
    tags_raw =  request.form.get('tags')
    if tags_raw is not None:
        tags_str1 = tags_raw.replace(" ", "")
        tags_str2 = tags_str1.split(',')

        for tag_str in tags_str2:
            if tag_str != "":
                tags.append(tag_str)

    # GROUPS
    # groups = []
    visibility = request.form.get('visibility')

    post.set_visibility(visibility)
    # hardcoded, one group only rn
    # if visibility == 'Public':
    #     groups.append(Group.query.get(1))
    # elif visibility == 'Friends':
    #     groups.append(user._groups[0]) # friends group
    #
    # groups.append(user._groups[1]) # just me group

    # TAGGING PEOPLE
    # In content, look for the string right after the @ sign
    if content:
        after_sign = content.split("@")
        # determine if string is a valid netid

        for str in after_sign:
            split_str = str.split(' ',  2)
            possible_netid = split_str[0]
            possible_user = User.query.get(possible_netid)

            if possible_user is not None:
                notif = Notification(user, possible_user, NType.TAGGED, post)
            elif len(split_str) > 1:
                possible_firstname = split_str[0]
                possible_lastname = split_str[1]

                p = db.session.query(User)
                p = p.filter(User.firstname == possible_firstname)
                p = p.filter(User.lastname == possible_lastname)

                for tagged_user in p.all():
                    notif = Notification(user, tagged_user, NType.TAGGED, post)

    if "image" in request.files:
        image = request.files["image"]
        if image.filename is not '':
            post.add_img(image)

    post.update_info(content, groups=[], tags=tags)

@page.route('/post/<int:postid>/delete', methods=['POST'])
@user_required
def delete_post(postid):
    post = Post.query.get(postid)
    post.delete()
    return redirect("/feed")


@page.route('/post/<int:postid>', methods=['GET'])
@user_required
def view_post(postid):
    post = Post.query.get(postid)
    if post is None:
        return render('message.html',
            title='Error',
            message="This post doesn't exist.")

    comments = post.get_comments()
    num_likers = len(post.get_likers())
    tags = post.get_tags()

    return render("post.html", post=post, comments=comments,
    num_likers = num_likers, tags=tags)


@page.route('/post/<int:postid>/comment', methods=['GET', 'POST'])
@user_required
def comment(postid):
    post = Post.query.get(postid)
    if post is None:
        return render('message.html',
            title='Error',
            message="This post doesn't exist.")

    if request.method=='GET':
        return render("post_comment.html", post=post)
    else:
        user = cur_user()
        content = request.form.get('content')

        comment = Comment(postid, content, user)

        if(post.creator is not user):
            notif = Notification(user, post.creator, NType.COMMENTED, post)

        db.session.commit()

        return redirect('/post/' + str(postid))

# @page.route('/post/<int:post_id>', methods=['GET'])
# def feed_post(post_id):
#     # # TODO:
#     return

@page.route('/post/<int:post_id>/<isLike>')
@user_required
def like(post_id, isLike):
    # # TODO:
    post = Post.query.get(post_id)
    if post is None:
        return render('message.html',
            title='Error',
            message="This post doesn't exist.")

    user = cur_user()

    if isLike == 'True':  #passing a string sorry
        post.add_like(user)
        if(post.creator is not user):
            notif = Notification(user, post.creator, NType.LIKED, post)
    else:
        post.unlike(user)

    db.session.commit()

    return redirect(request.referrer)

# Might need FIXME
@page.route('/post/<int:post_id>/tag')
@user_required
def add_tag(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return render('message.html',
            title='Error',
            message="This post doesn't exist.")

    tag_str = request.form.get('content')

    post.add_tag_str(tag_str)

    return redirect(request.referrer)

# def get_tag(post_id):
#     post = Post.query.get(post_id)
#     tags = post.get_tags()
#
#     return redirect(request.referrer)

# @page.route('/post/<int:post_id>/likers', methods=['GET'])
# def likers(post_id):
#     post = Post.query.get(postid)
#     likers = post.get_likers()
#     likersStr = str(likers)
#
#     return render('message.html',
#         title='Success',
#         message=likersStr)

# @page.route('/post/<int:post_id>/num-likers', methods=['GET'])
