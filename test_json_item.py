import json
from bokeh.embed import json_item
with open('./data/file_json.json', 'r') as f:
    item = json.load(f)
    print(item)
    json_item(item)


