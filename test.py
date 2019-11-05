# from orangepages.views.testsearch import testsearch_local

# testsearch_local("sa st")

from orangepages import app
app.run(host='0.0.0.0', port=5000, debug=True)