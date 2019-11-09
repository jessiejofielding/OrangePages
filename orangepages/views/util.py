# Helper functions for other views


from flask import request, render_template

from orangepages.models.models import User


#-----------------------------------------------------------------------

# user netid is stored in a cookie for /test pages that don't use CAS 

# Set current user cookie in response.
def set_uid(response, netid):
    if netid is None:
        response.set_cookie('uid', expires=0)
    else:
        response.set_cookie('uid', netid)
    return response

# Get current user from cookie.
def cur_user():
    uid = cur_uid()
    if uid is None:
        return None
    return User.query.get(uid)

# Get current netid from cookie.
def cur_uid():
    return request.cookies.get('uid')


# Wrapper function for render_template to automatically include
# current user (since navbar always needs it)
def render(*args, **kwargs):
    return render_template(args, **kwargs, user=cur_user())
