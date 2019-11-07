from orangepages.views.test import testsearch_local

# testsearch_local("elise")

from orangepages import app
app.run(host='0.0.0.0', port=5000, debug=True)
