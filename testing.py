import json

with open('keyfeed.json','r') as read_file:
    data = json.load(read_file)

print(json.dumps(data, indent=4))
