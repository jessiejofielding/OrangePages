# For testing with templates/test/*.html

from flask import request, make_response, url_for, redirect
from flask import Blueprint, render_template

from orangepages.models.models import db, User
from orangepages.views.util import cur_user, cur_uid, set_uid, render

page = Blueprint('test', __name__, 
    template_folder='../templates/test', url_prefix='/test')

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
    response = make_response(render('logout.html'))
    return set_uid(response, None)


@page.route('/feed', methods=['GET'])
def feed():
    posts = cur_user().get_feed()
    return render('feed.html', posts=posts)


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
    db.session.add(user)
    db.session.commit()

    return render('profile_created.html')


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

    return render('profile_edited.html')
