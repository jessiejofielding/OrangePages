from flask import request, make_response, redirect
from flask import Blueprint, render_template
from orangepages.models.models import db, User
from flask_cas_fix import login_required
from sqlalchemy import exc
from orangepages import app
import os.path

from orangepages.views.util import cur_user, cur_uid, render, user_required



page = Blueprint('user_page', __name__)


# def upload_pic(image):
#     if request.method == "POST":
#         if request.files:
#             image = request.files["image"]

@page.route('/profile/<string:lookup_id>', methods=['GET'])
@user_required
def view_profile(lookup_id):

    # img_path = app.config["IMAGE_UPLOADS_RELATIVE"] + lookup_id + "_pic.jpeg"
    # img_path_check = app.config["IMAGE_UPLOADS"] + lookup_id + "_pic.jpeg"
    #
    # if os.path.isfile(img_path_check):
    #     img_path = app.config["IMAGE_UPLOADS_RELATIVE"] + lookup_id + "_pic.jpeg"
    # else:
    #     img_path = 'https://res.cloudinary.com/hcfgcbhqf/image/upload/c_fill,h_120,w_120,g_face,r_10/r3luksdmal8hwkvzfc25.png'

    if cur_uid() == lookup_id:
        # img_path = app.config["IMAGE_UPLOADS_RELATIVE"] + lookup_id
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

    if "image" in request.files:
        image = request.files["image"]
        if image.filename is not '':
            print("IMAGE", image)
            user.add_img(image)

    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session().rollback()

    return render('message.html',
        title='Success',
        message='You have successfully registered!')




@page.route('/edit-user', methods=['GET', 'POST'])
@user_required
def edit_user():

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

        if "image" in request.files:
            image = request.files["image"]
            if image.filename is not '':
                print("IMAGE", image)
                cur_user().add_img(image)

        db.session.commit()

    return redirect('/profile/'+cur_uid())

    return render('message.html',
        title='Success',
        message='You have successfully edited your profile!')



@page.route('/notifications', methods=['GET'])
@user_required
def view_notifs():
    user = cur_user()

    # Order of next few lines matter, pls don't rearrange
    notifs = user.notifs.all()
    unread_count = user._unread_notifs
    user.reset_unread()
    for notif, i in zip(notifs, range(unread_count)):
        notif.unread = True # Do not commit to db session

    return render('notifs.html', notifs=notifs)


@page.route('/clear-notifs', methods=['GET'])
@user_required
def clear_notifs():
    user = cur_user()

    notifs = user.notifs.all()
    for notif in notifs:
        notif.delete()

    db.session.commit()
    return redirect(request.referrer)
