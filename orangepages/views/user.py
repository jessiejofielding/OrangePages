from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User
from flask_cas_fix import login_required
from sqlalchemy import exc

from orangepages.views.util import cur_user, cur_uid, render



page = Blueprint('user', __name__)


@page.route('/profile/<string:lookup_id>', methods=['GET'])
#@login_required
def view_profile(lookup_id):

    if cur_user() is None:
        return redirect('/create-user')

    if cur_uid() == lookup_id:
        return render('profile_user.html')

    lookup = User.query.get(lookup_id)
    if lookup is None:
        return render('message.html',
            title='Error',
            message="This user doesn't exist.")
        
    friends_list = lookup.friend_list()

    return render('profile.html', lookup=lookup,friends_list=friends_list)




@page.route('/create-user', methods=['GET', 'POST'])
#@login_required
def create_user():

    if cur_user() is not None:
        return redirect('/edit-user')

    if request.method=='GET':
        return render('profile_create.html')


    # Get form fields
    netid = cur_uid()
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    rescollege = request.form.get('rescollege')
    school = request.form.get('school') # this is AB or BSE lol
    major = request.form.get('major')
    year = request.form.get('year')
    food = request.form.get('food')
    building = request.form.get('building')
    room = request.form.get('room')
    hometown = request.form.get('hometown')
    state = request.form.get('state')
    country = request.form.get('country')
    team = request.form.get('team')
    groups = request.form.get('groups')
    certificate = request.form.get('certificate')
    birthday = request.form.get('birthday')

    use_photo = request.form.get('photo')

    affiliations = []

    if request.form.get('rca'):
        affiliations.append('RCA')
    if request.form.get('paa'):
        affiliations.append('PAA')
    if request.form.get('share_peer'):
        affiliations.append('Share Peer')
    
    email = netid + "@princeton.edu"

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
#@login_required
def edit_user():
    if cur_user() is None:
        return redirect('/create-user')

    if request.method=='POST':
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

    return redirect('/profile/'+cur_uid())

    return render('message.html',
        title='Success',
        message='You have successfully edited your profile!')



@page.route('/notifications', methods=['GET'])
#@login_required
def view_notifs():
    user = cur_user()

    if user is None:
        return redirect('/create-user')

    # Order of next few lines matter, pls don't rearrange
    notifs = user.notifs.all()
    unread_count = user._unread_notifs
    user.reset_unread()
    for notif, i in zip(notifs, range(unread_count)):
        notif.unread = True # Do not commit to db session 

    return render('notifs.html', notifs=notifs)


@page.route('/clear-notifs', methods=['GET'])
#@login_required
def clear_notifs():
    user = cur_user()
    if user is None:
        return redirect('/create-user')

    notifs = user.notifs.all()
    for notif in notifs:
        notif.delete()

    db.session.commit()
    return redirect(request.referrer)


