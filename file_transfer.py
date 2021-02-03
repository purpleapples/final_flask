from flask import Flask, Request, request
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

@app.route('/visual/date/cnt')
def getDateCntGraph():
    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.visual_data
    return {'data':  list(collection.find({'graph_sort': 'data_count_graph'}, projection={"_id": 0}).limit(1))}

@app.route('/visual', methods=['POST'])
def getVariableAndPutBokeh():

    """
    :param YearweekNum: 년도+주차숫자
    :return: 통계시각화데이터
    """
    json_data = request.get_json()# 전송한 json data
    print(json_data)
    # 년도
    year = json_data['year']
    # 주차
    weekNum = json_data['weekNum']
    # graph 종류
    graphSort = json_data['graphSort']

    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.visual_data
    # $regex :년도 닮음 검색

    data = list(collection.find({"date": {"$regex": year, "$options": "i"},
                                 # 주차 조건 추가 필요

                                 # graph 종류 조건 추가 필요
                                 # "graph_sort" : graph_sort
                                 },
                                projection={"_id": 0} # objectId 제외
                                )
                )
    # temporary data diet
    data = data[0]
    return {'data':  data}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
