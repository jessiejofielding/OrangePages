from flask import request, make_response
from flask import Blueprint, render_template
from orangepages.models.models import User
# from orangepages import cas
# from flask_cas import login
# from flask_cas import logout
# from flask_cas import login_required
# from flask_login import current_user, login_required


page = Blueprint('general', __name__)


@page.route('/', methods=['GET'])
@page.route('/feed', methods=['GET'])
def feed():
    import CASClient
    C = CASClient.CASClient()
    netid = C.Authenticate()
    print(C)
    print(netid)
    # # TODO:
    # username = cas.username
    # attributes = cas.attributes
    # print(username)
    netid = 'jexample'  # TODO: make this current_user
    user = User.query.get(netid)
    posts = user.get_feed()
    return render_template('index.html', posts=posts)

# @page.route("/secure")
# @login_required
# def secure():
#     username = cas.username
#     # attributes = cas.attributes
#     print(username)
#     # logging.info('CAS username: %s', username)
#     # logging.info('CAS attributes: %s', attributes)

#     return render_template('404.html', cas=cas)
