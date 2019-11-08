from orangepages import app
import os
print(os.environ.get('PORT'))
print(os.environ.get('$PORT'))
app.run()
print(os.environ.get('PORT'))