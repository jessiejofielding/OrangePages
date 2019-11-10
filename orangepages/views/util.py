# Helper functions for other views

from flask import request, render_template, redirect

from orangepages.models.models import User
from orangepages import cas



#-----------------------------------------------------------------------


# LOCAL TESTING: Set current user cookie in response.
def set_uid(response, netid):
    if netid is None:
        response.set_cookie('uid', expires=0)
    else:
        response.set_cookie('uid', netid)
    return response


# Get current User.
def cur_user():
    uid = cur_uid()
    if uid is None:
        return None
    return User.query.get(uid)

# Get current netid.
def cur_uid():
    netid = cas.username

    # LOCAL TESTING: use netid stored in cookie instead of cas
    if netid is None:
        return request.cookies.get('uid') 

    return netid[0]


# If current user is new, redirect them to user creation page.
def check_newuser():
    if cur_user() is None:
        return redirect('/create-user')



# Wrapper function for render_template to automatically include
# current user (since navbar always needs it)
def render(*args, **kwargs):
    return render_template(args, **kwargs, user=cur_user())
