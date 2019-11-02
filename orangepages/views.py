from flask import Flask, render_template
from flask_login import current_user, login_required

@app.route('/', methods=['GET'])
@app.route('/feed', methods=['GET'])
@login_required
def feed():
    # # TODO:

@app.route('/search', methods=['GET'])
def search():
    # # TODO:
    return render_template('search_preview.html',
    user_preview_list=user_preview_list)

@app.route('/post/<int:post_id>', methods=['GET'])
def feed_post(post_id):
    # # TODO:

@app.route('/create-post', methods=['POST'])
def create_post():
    # # TODO:

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def comment(post_id):
    # # TODO:

@app.route('/post/<int:post_id>/like', methods=['POST'])
def like(post_id):
    # # TODO:

@app.route('/user/<string:lookup_id>', methods=['GET'])
def view_profile(lookup_id):
    # # TODO:

@app.route('/create-user', methods=['POST'])
def create_user():
    # # TODO:

@app.route('/edit-user', methods=['PUT'])
def edit_user():
    # # TODO:
