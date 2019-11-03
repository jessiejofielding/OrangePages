from flask import request, make_response
from flask import Blueprint, render_template
# from flask_login import current_user, login_required


page = Blueprint('post', __name__)


@page.route('/post/<int:post_id>', methods=['GET'])
def feed_post(post_id):
    # # TODO:
    return

@page.route('/create-post', methods=['POST'])
def create_post():
    # # TODO:
    return

@page.route('/post/<int:post_id>/comment', methods=['POST'])
def comment(post_id):
    # # TODO:
    return

@page.route('/post/<int:post_id>/like', methods=['POST'])
def like(post_id):
    # # TODO:
    return