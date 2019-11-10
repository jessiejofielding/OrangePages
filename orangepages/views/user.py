from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User
from flask_cas_fix import login_required

from orangepages.views.util import cur_user, cur_uid, check_newuser, render



page = Blueprint('user', __name__)


@page.route('/profile/<string:lookup_id>', methods=['GET'])
@login_required
def view_profile(lookup_id):
    check_newuser()
    user = User.query.get(lookup_id) 
    return render_template('profile.html', user=user)




@page.route('/create-user', methods=['GET', 'POST'])
@login_required
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
    db.session.add(user)
    db.session.commit()

    return render('message.html', 
        title='Success',
        message='You have successfully registered!')




@page.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edit_user():
    check_newuser()

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


