import json

with open('./mint.json','r') as json_file:
    data = json.load(json_file)

print(type(data))
len(data.keys())