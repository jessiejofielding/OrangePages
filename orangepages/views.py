from flask import Flask, render_template
from flask_login import current_user, login_required

@app.route('/', methods=['GET'])
@app.route('/feed', methods=['GET'])
@login_required
def feed():
    # # TODO:

@app.route('/feed/post', methods=['GET'])
def feed_post():
    # # TODO:

@app.route('/create-post', methods=['POST'])
def create_post():
    # # TODO:

@app.route('/post=_/comment', methods=['POST'])
def comment():
    # # TODO:

@app.route('/post=_/like', methods=['POST'])
def like():
    # # TODO:

@app.route('/search', methods=['GET'])
def search():
    # # TODO:

@app.route('/view-profile', methods=['GET'])
def view_profile():
    # # TODO:

@app.route('/create-user', methods=['POST'])
def create_user():
    # # TODO:

@app.route('/edit-user', methods=['PUT'])
def edit_user():
    # # TODO:

@app.route('/create-user/')
def create_user():
    # # TODO:
