from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User, Notification
from flask_cas_fix import login_required
from sqlalchemy import exc
from orangepages import app
import os.path

from orangepages.views.util import cur_user, cur_uid, render, user_required



page = Blueprint('user_page', __name__)



@page.route('/profile/<string:lookup_id>', methods=['GET'])
@user_required
def view_profile(lookup_id):

    if cur_uid() == lookup_id:
        user = cur_user()
        names = ['netid', 'firstname', 'lastname', 'email', 'hometown',
            'state', 'country', 'year', 'major', 'rescollege', 'school',
            'room', 'building', 'food', 'team', 'activities',
            'certificate', 'birthday']
        privs = user.group_to_priv(user.get_attr_priv())
        cur_privacy = {}
        for name, priv in zip(names, privs):
            cur_privacy[name] = priv
            # print(name + " " + priv)
        return render('profile_user.html', cur_privacy = cur_privacy)

    lookup = User.query.get(lookup_id)
    if lookup is None:
        return render('message.html',
            title='Error',
            message="This user doesn't exist.")

    friends_list = lookup.friend_list()

    # maps attr to attr content for lookup user, with consideration of lookup
    # user's privacy settings
    lookup_priv = cur_user().lookup_user(lookup_id)

    return render('profile.html', lookup_priv=lookup_priv,
    lookup=lookup,friends_list=friends_list)




@page.route('/create-user', methods=['GET', 'POST'])
#@login_required
def create_user():

    if cur_user() is not None:
        return redirect('/edit-user')

    if request.method=='GET':
        from tigerbook import get_info
        netid = cur_uid()
        info = get_info(netid)
        first = info['first_name']
        last = info['last_name']
        class_year = info['class_year']
        rescollege = info['res_college']
        major_code = info['major_code'].upper()
        major_type = info['major_type']
        return render('profile_create.html', first_name=first, last_name=last, 
                        class_year=class_year, res_college=rescollege, major_type=major_type,
                        major_code=major_code)

    # Get form fields
    # from tigerbook import get_info
    netid = cur_uid()
    # info = get_info(netid)
    # return render('message.html',
    #     title='Success',
    #     message=info)

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
    activities = request.form.get('groups')
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
    user = User(netid)
    user.update_public_info(firstname,lastname, email, rescollege, school, major, year)
    user.update_optional_info(hometown, state, country, room, building, food,
    team, activities, certificate, birthday, affiliations)

    if use_photo:
        # TODO: tigerbook API
        pass

    if "image" in request.files:
        image = request.files["image"]
        if image.filename is not '':
            # print("IMAGE", image)
            user.add_img(image)

    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except exc.IntegrityError as e:
    #     db.session().rollback()

    return render('message.html',
        title='Success',
        message='You have successfully registered!')




@page.route('/edit-user', methods=['POST'])
@user_required
def edit_user():
    user = cur_user()

    # Get attribute fields
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
    rescollege = request.form.get('rescollege')
    school = request.form.get('school')
    food = request.form.get('food')
    team = request.form.get('team')
    activities = request.form.get('activities')
    certificate = request.form.get('certificate')
    birthday = request.form.get('birthday')
    affiliations = []

    # Update attributes
    user.update_public_info(firstname,lastname, email, rescollege, school, major, year)
    user.update_optional_info(hometown, state, country, room, building, food,
    team, activities, certificate, birthday, affiliations)

    if "image" in request.files:
        image = request.files["image"]
        if image.filename is not '':
            print("IMAGE", image)
            user.add_img(image)

    
    # Get privacy fields
    hometown_priv = request.form.get('hometown_priv')
    state_priv = request.form.get('state_priv')
    country_priv = request.form.get('country_priv')
    major_priv = request.form.get('major_priv')
    room_priv = request.form.get('room_priv')
    building_priv = request.form.get('building_priv')
    rescollege_priv = request.form.get('rescollege_priv')
    school_priv = request.form.get('school_priv')
    food_priv = request.form.get('food_priv')
    team_priv = request.form.get('team_priv')
    activities_priv = request.form.get('activities_priv')
    certificate_priv = request.form.get('certificate_priv')
    birthday_priv = request.form.get('birthday_priv')

    # Update privacy 
    user.update_privacy(hometown_priv, state_priv, country_priv, 
        major_priv, rescollege_priv, school_priv, room_priv, 
        building_priv, food_priv, team_priv, activities_priv, 
        certificate_priv, birthday_priv)

    return redirect('/profile/'+cur_uid())



@page.route('/notifications', methods=['GET', 'POST'])
@user_required
def view_notifs():
    user = cur_user()
    notifs = user.notifs.all()
    if request.method=='POST':
        return render('notifs.html', notifs=notifs)
    return render('notifs_page.html', notifs=notifs)


@page.route('/notif/<int:nid>', methods=['GET'])
@user_required
def notif_link(nid):
    user = cur_user()

    notif = Notification.query.get(nid)
    if notif.target is not user:
        return redirect(request.referrer)

    if notif.unread:
        notif.mark_read()
    return redirect(notif.link_to())



@page.route('/clear-notifs', methods=['GET'])
@user_required
def clear_notifs():
    user = cur_user()

    notifs = user.notifs.all()
    for notif in notifs:
        notif.delete()

    return redirect(request.referrer)

@page.route('/clear-notif/<int:id>', methods=['POST'])
@user_required
def clear_single_notif(id):
    user = cur_user()
    print('clearing notif id', id)

    notif = Notification.query.get(id)

    if notif.target is user:
        notif.delete()

    return redirect(request.referrer)

