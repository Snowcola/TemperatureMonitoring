import requests

headers = {'Content-type': 'application/json'}
payload = {'temp': 9}
url = "http://127.0.0.1:5000/api/v1/submit_temp"

r = requests.post(url, json=payload, headers=headers)

print(r.content)