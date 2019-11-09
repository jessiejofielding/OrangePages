from flask import request, make_response
from flask import Blueprint, render_template

from flask_cas_fix import login, logout, login_required

from orangepages.models.models import User
from orangepages import cas
from orangepages.views.util import render



page = Blueprint('error', __name__)



@page.app_errorhandler(404)
def not_found(e):
    return render('404.html'), 404
