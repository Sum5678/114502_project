import requests
import json

# URL of the server
url = 'http://localhost:5000/process'

# JSON data to be sent in the request body
data = {
    'input_data': 'example_data'
}

# Sending POST request with JSON data
response = requests.post(url, json=data)

# Printing the response
print(response.json())