import requests
import json

url = "http://localhost:5000/api/copilotkit/info"
try:
    response = requests.post(url, json={})
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
