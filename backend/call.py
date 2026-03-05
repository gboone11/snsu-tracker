import requests

endpoint = "http://127.0.0.1:8000/clear-data"
data = {

}

response = requests.post(endpoint)
print(response.json())

