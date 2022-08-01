import requests
import json

json_object = json.dumps(
  [
    'HOOD',
    'GOOG',
    'AMZN',
    'BABA',
    'NOW',
  ]
)

print(requests.get('http://localhost:5000/winners_from_list', json=json_object).json())