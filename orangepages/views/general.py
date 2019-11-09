from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User
from orangepages import cas
from flask_cas_fix import login
from flask_cas_fix import logout
from flask_cas_fix import login_required
# from flask_login import current_user, login_required


page = Blueprint('general', __name__)


@page.route('/', methods=['GET'])
@page.route('/feed', methods=['GET'])
@login_required # TODO: make other pages also require login?
def feed():
    netid = cas.username[0]  # TODO: save current user as part of the session maybe? or as cookies bc they seem simpler tbd
    user = User.query.get(netid)
    posts = user.get_feed()
    return render_template('index.html', posts=posts, user=user)

