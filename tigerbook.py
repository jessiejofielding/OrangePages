import hashlib
import random
import requests
import json
import os
from base64 import b64encode
from datetime import datetime


def get_info(netid):
    url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates/' + netid
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    created = created.encode()
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
    nonce = nonce.encode()
    username = os.environ.get('TIGERBOOK_USER').encode()
    password = os.environ.get('TIGERBOOK_SECRET').encode()    # use your own from /getkey
    generated_digest = b64encode(hashlib.sha256(nonce + created + password).digest())
    headers = {
        b'Authorization': b'WSSE profile="UsernameToken"',
        b'X-WSSE': b'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, b64encode(nonce), created)
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else: return None
    


if __name__ == "__main__":
    key = get_info('jjf4')
    for thing in key:
        print(thing + ":\t" + str(key[thing])) 
    