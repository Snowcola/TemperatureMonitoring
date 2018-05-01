import requests

headers = {"Content-type": "application/json"}
payload = {'temp': 9}
url = "http://127.0.0.1:5000"

r = requests.post(url, data=payload, headers=headers)

print(r.content)