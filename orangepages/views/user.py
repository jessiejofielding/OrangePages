from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User
from flask_cas_fix import login_required

# from flask_login import current_user, login_required


page = Blueprint('user', __name__)


@page.route('/profile/<string:lookup_id>', methods=['GET'])
#@login_required
def view_profile(lookup_id):
    user = User.query.get(lookup_id)
    return render_template('profile.html', user=user)

@page.route('/create-user', methods=['POST'])
def create_user():
    # # TODO:
    return

@page.route('/edit-user', methods=['PUT'])
def edit_user():
    # # TODO:
    return