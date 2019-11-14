# For testing with templates/test/*.html

from flask import request, make_response, url_for, redirect
from flask import Blueprint, render_template
from sqlalchemy import exc

from orangepages.models.models import db, User, Group, Post, Comment
from orangepages.views.util import cur_user, cur_uid, set_uid, render

page = Blueprint('test', __name__,
    template_folder='../templates/test', url_prefix='/test')

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

        return render('message.html',
            title='Success',
            message='You have successfully added ur comment. yay. congrats. now go eat a popsickle')

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

    return render("post_created.html")


#-----------------------------------------------------------------------
# search.py


@page.route('/search')
def testsearch():
    query = request.args.get('query')

    query_list = query.split()
    user_preview_list = User.search(*query_list)

    return render_template('search.html', query=query,
    user_preview_list=user_preview_list)

def testsearch_local(query):
    query_list = query.split()
    user_preview_list = User.search(*query_list)
    for user in user_preview_list:
        print(user)

#-----------------------------------------------------------------------
# general.py

@page.route('/')
@page.route('/page')
def testpage():
    if cur_user() is None:
        return render('page.html')
    return redirect('feed')



@page.route('/login')
def login():
    netid = request.args.get('netid')

    if (netid is None) or (netid.strip() == ''):
        return render('login.html')

    user = User.query.get(netid)
    if user is None:
        response = make_response(redirect('create-user'))
    else:
        response = make_response(redirect('feed'))
    return set_uid(response, netid)


@page.route('/logout')
def logout():
    response = make_response(render('message.html',
        title='Logged out',
        message='You have been successfully logged out.'))
    return set_uid(response, None)


@page.route('/feed', methods=['GET'])
def feed():
    posts = cur_user().get_feed()
    # for p in posts:
    #     print(p)
    #return render('all_posts.html', posts=posts)
    return render('test/feed.html', posts=posts)


#-----------------------------------------------------------------------
# user.py

@page.route('/profile/<string:lookup_id>', methods=['GET'])
def view_profile(lookup_id):
    user = User.query.get(lookup_id)
    return render_template('test/profile.html', user=user)


@page.route('/create-user', methods=['GET', 'POST'])
def create_user():

    if request.method=='GET':
        return render('profile_create.html')


    # Get form fields
    netid = cur_uid()
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    hometown = request.form.get('hometown')
    state = request.form.get('state')
    country = request.form.get('country')
    year = request.form.get('year')
    major = request.form.get('major')
    room = request.form.get('room')
    building = request.form.get('building')

    # Create and update user
    user = User(netid, firstname, lastname, email)
    user.update_optional_info(firstname,lastname,email,
        hometown,state,country,year,major,room,building)

    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session().rollback()

    return render('message.html',
        title='Success',
        message='You have successfully registered!')


@page.route('/edit-user', methods=['GET', 'POST'])
def edit_user():

    if request.method=='GET':
        return render('profile_edit.html')

    # Get form fields
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    hometown = request.form.get('hometown')
    state = request.form.get('state')
    country = request.form.get('country')
    year = request.form.get('year')
    major = request.form.get('major')
    room = request.form.get('room')
    building = request.form.get('building')

    # Update user
    cur_user().update_optional_info(firstname,lastname,email,
        hometown,state,country,year,major,room,building)
    db.session.commit()

    return render('message.html',
        title='Success',
        message='You have successfully edited your profile!')
