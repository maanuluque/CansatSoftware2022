import os
import json

with open('data.json') as file:
    json_data = json.load(file)
    
data = json.loads(json_data)
print("Key 1: " + data["key1"])
print("Key 2: " + data["key2"])