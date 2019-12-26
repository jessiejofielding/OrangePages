from flask import request, make_response
from flask import Blueprint, render_template

from flask_cas_fix import login, logout, login_required

from orangepages.models.models import User
from orangepages import cas
from orangepages.views.util import render



page = Blueprint('error', __name__)



@page.app_errorhandler(404)
def not_found(e):
    return render('message.html',
            title='Oops.',
            message="This page doesn't exist."), 404

@page.app_errorhandler(500)
def server_error(e):
    return render('message.html',
            title='A server error occurred.',
            message="Please try again later?"), 500

@page.app_errorhandler(405)
def not_allowed(e):
    return render('message.html',
            title='Not allowed',
            message="leave"), 405
