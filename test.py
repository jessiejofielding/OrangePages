# from orangepages.views.test import likers_local, like_local
#
# likers_local(2)
# like_local('jexample', 2, True)
# likers_local(2)
# testsearch_local("elise")

from orangepages import app
app.run(host='0.0.0.0', port=5000, debug=True)
