from flask import request, redirect, make_response
from flask import Blueprint, render_template, send_from_directory
from orangepages.models.models import db, User, Group, Post, Comment, Tag, NType, Notification
from orangepages.views.util import cur_user, cur_uid, render
from orangepages import app
import os
# from flask_login import current_user, login_required


page = Blueprint('post', __name__)

@page.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method=='GET':
        return render('post_create.html')

    user = cur_user()
    content = request.form.get('content')

    # Parse tags and add them - list of tag STRINGS
    tags = []
    tags_raw =  request.form.get('tags')
    if tags_raw is not None:
        tags_str1 = tags_raw.replace(" ", "")
        tags_str2 = tags_str1.split(',')

        for tag_str in tags_str2:
            if tag_str != "":
                tags.append(tag_str)

    # TO FIX
    groups = []
    visibility = request.form.get('visibility')
    # hardcoded, one group only rn
    if visibility == 'Public':
        groups.append(Group.query.get(1))
    elif visibility == 'Friends':
        groups.append(user._groups[0]) # friends group

    groups.append(user._groups[1]) # just me group


    post = Post(content, user, groups, tags)
    db.session.add(post)
    db.session.commit()

    # In content, look for the string right after the @ sign
    after_sign = content.split("@")
    # determine if string is a valid netid

    for str in after_sign:
        split_str = str.split(' ',  2)
        possible_netid = split_str[0]
        possible_user = User.query.get(possible_netid)
        # print("possible_user", possible_user)
        #
        # print("len(split_str)", len(split_str))
        # print(split_str)

        if possible_user is not None:
            notif = Notification(user, possible_user, NType.TAGGED, post)
            db.session.add(notif)
            db.session.commit()
        elif len(split_str) > 1:
            possible_firstname = split_str[0]
            possible_lastname = split_str[1]
            # print(possible_firstname, possible_lastname)

            p = db.session.query(User)
            p = p.filter(User.firstname == possible_firstname)
            p = p.filter(User.lastname == possible_lastname)

            for tagged_user in p.all():
                notif = Notification(user, tagged_user, NType.TAGGED, post)
                db.session.add(notif)
                db.session.commit()

    if "image" in request.files:
        image = request.files["image"]
        if image.filename is not '':
            post.add_img(image)

    return redirect("/feed")

@page.route('/post/<int:postid>', methods=['GET'])
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
        db.session.add(comment)

        if(post.creator is not user):
            notif = Notification(user, post.creator, NType.COMMENTED, post)
            db.session.add(notif)

        db.session.commit()

        return redirect('/post/' + str(postid))

# @page.route('/post/<int:post_id>', methods=['GET'])
# def feed_post(post_id):
#     # # TODO:
#     return

@page.route('/post/<int:post_id>/<isLike>')
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
            db.session.add(notif)

    else:
        post.unlike(user)

    db.session.commit()

    return redirect(request.referrer)

# Might need FIXME
@page.route('/post/<int:post_id>/tag')
def add_tag(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return render('message.html',
            title='Error',
            message="This post doesn't exist.")

    tag_str = request.form.get('content')

    post.add_tag_str(tag_str)
    # tag = Tag(tag_str)
    # post.add_tag(tag)

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

# uploads an image
@page.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return redirect(request.referrer)

    return render_template("/upload_image.html")

@page.route('/uploads/<filename>')
def uploaded_file(filename):
    name = app.config["IMAGE_UPLOADS_RELATIVE"] + filename
    # print(name)
    return render_template("img.html", img_name=name)
