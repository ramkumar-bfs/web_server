import requests

url = "http://localhost:8000/submit_nuke_copycat_render"
payload = {"message": "Hello from API"}
response = requests.post(url, json=payload)
print(response.json())
