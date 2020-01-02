from datetime import datetime
from flask import redirect, request
from flask import Blueprint
from flask_cas_fix import login, logout, login_required
from orangepages.models.models import User
from orangepages.views.util import cur_user, render, user_required


page = Blueprint('general', __name__)



@page.route('/')
def home():
    if cur_user() is None:
        return render('index.html')
    return redirect('/feed')


@page.route('/login')
@login_required
def login():
    if cur_user() is None:
        return redirect('/create-user')
    return redirect('/feed')


@page.route('/logout')
def logout_route():
    return logout() # (cas logout)


# @page.route('/feed', methods=['GET'])
# @user_required
# def feed():
#     posts = cur_user().get_feed()
#     return render('feed.html', posts=posts)


# get initial feed
@page.route('/feed', methods=['GET'])
@user_required
def feed():
    t = datetime.utcnow()
    posts = cur_user().feed_next(t)
    t_last = get_t_last(posts, t)
    return render('feed.html', posts=posts, t_first=t, t_last=t_last)

# refresh posts currently displayed on feed (timestamps, comments)
@page.route('/feed-refresh', methods=['POST'])
@user_required
def feed_refresh():
    t_first = request.form.get('t_first')
    t_last = request.form.get('t_last')
    posts = cur_user().feed_range(t_first, t_last)
    return render('feed_posts.html', posts=posts, t_last=t_last,
        t_first=t_first)

# get older posts
@page.route('/feed-next', methods=['POST'])
@user_required
def feed_next():
    t_first = request.form.get('t_first')
    time = request.form.get('t_last')
    posts = cur_user().feed_next(time)
    t_last = get_t_last(posts, time)
    return render('feed_posts.html', posts=posts, t_last=t_last,
        t_first=t_first)

# check for new posts
@page.route('/feed-check', methods=['POST'])
@user_required
def feed_check():
    time = request.form.get('t_first')
    posts = cur_user().feed_new(time)
    return str(len(posts))

# get new posts
@page.route('/feed-new', methods=['POST'])
@user_required
def feed_new():
    time = request.form.get('t_first')
    t_last = request.form.get('t_last')
    posts = cur_user().feed_new(time)
    return render('feed_posts.html', posts=posts, t_last=t_last,
        t_first=datetime.utcnow())



# util
def get_t_last(posts, t):
    if len(posts) > 0:
        return posts[-1].date
    else:
        return t
