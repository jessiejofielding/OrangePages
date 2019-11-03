from flask import request, make_response
from flask import Blueprint, render_template
# from flask_login import current_user, login_required


page = Blueprint('general', __name__)


@page.route('/', methods=['GET'])
@page.route('/feed', methods=['GET'])
# @login_required
def feed():
    # # TODO:
    return