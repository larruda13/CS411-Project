import json

def parse_json(r):
    r = json.loads(r)
    output = parsed_json['artists']['genres'][0]