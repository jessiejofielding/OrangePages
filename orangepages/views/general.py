from flask import redirect
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


@page.route('/feed', methods=['GET'])
@user_required
def feed():
    posts = cur_user().get_feed()
    return render('feed.html', posts=posts)
