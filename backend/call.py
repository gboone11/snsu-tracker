import requests

endpoint = "http://127.0.0.1:8000/users"
data = {
    "username": "jodoe",
    "full_name": "John Doe",
    "initials": "JD",
    "team_name": "Operations"
}

response = requests.post(endpoint, json=data)
print(response.json())

response = requests.get(endpoint)
print(response.json())

response = requests.delete(f"{endpoint}/1")
print(response.json())

response = requests.get(endpoint)
print(response.json())