from flask import Flask
from bokeh.embed import json_item
from flask_cors import CORS
from pymongo import MongoClient
app = Flask(__name__)
CORS(app)

@app.route('/test/data')
def transfort_data():
    import json
    with open('./data/file_json.json', 'r') as f:
        item = json.load(f)

    return item

@app.route('/test/data2')
def load_visualization_data():
    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.visual_data
    return {'data':  list(collection.find({}, projection={"_id": 0}).limit(1))}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
