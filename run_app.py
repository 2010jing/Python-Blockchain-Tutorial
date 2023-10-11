import requests
import json

url1 = "http://127.0.0.1:8001/register_with"
url2 = "http://127.0.0.1:8002/register_with"

payload = json.dumps({
  "node_address": "http://127.0.0.1:8000"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url1, headers=headers, data=payload)
print(response.text)
response = requests.request("POST", url2, headers=headers, data=payload)

print(response.text)

from app import app

app.run(debug=True)