# login
# 传入的参数
import pprint

import requests

payload = {
    'username': 'moirayang',
    'password': '1234567890'
}

response = requests.post('http://localhost:8000/mgr/signin', data=payload)

pprint.pprint(response.json())
