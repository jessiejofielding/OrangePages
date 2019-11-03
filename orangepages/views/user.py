from flask import request, make_response
from flask import Blueprint, render_template
# from flask_login import current_user, login_required


page = Blueprint('user', __name__)


@page.route('/user/<string:lookup_id>', methods=['GET'])
def view_profile(lookup_id):
    # # TODO:
    return

@page.route('/create-user', methods=['POST'])
def create_user():
    # # TODO:
    return

@page.route('/edit-user', methods=['PUT'])
def edit_user():
    # # TODO:
    return