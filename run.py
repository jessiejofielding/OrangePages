from orangepages import app
import os
temp = os.environ.get('PORT')
print(temp)
app.run(host='0.0.0.0', port=int(temp))
