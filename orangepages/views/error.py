from flask import request, make_response
from flask import Blueprint, render_template

from flask_cas_fix import login, logout, login_required

from orangepages.models.models import User
from orangepages import cas
from orangepages.views.util import render, user_required



page = Blueprint('error', __name__)



@page.app_errorhandler(404)
@user_required
def not_found(e):
    return render('message.html',
            title='Oops.',
            message="This page doesn't exist."), 404

@page.app_errorhandler(500)
@user_required
def server_error(e):
    return render('message.html',
            title='A server error occurred.',
            message="Please try again later."), 500

@page.app_errorhandler(405)
@user_required
def bad_method(e):
    return render('message.html',
            title='Bad method',
            message="This request method has been disabled."), 405

@page.app_errorhandler(403)
@user_required
def not_allowed(e):
    return render('message.html',
            title='Not allowed',
            message="You are unauthorized to access this content."), 403
