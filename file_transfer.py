from flask import Flask, request, jsonify
from bokeh.embed import json_item
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/visual', methods=['POST'])
def getVariableAndPutBokeh():

    """
    :param YearweekNum: 년도+주차숫자
    :return: 통계시각화데이터
    """
    json_data = request.get_json()# 전송한 json data
    print("data 확인", json_data)
    # 년도
    year = json_data['year']
    # 월
    month = json_data['month']

    # 주차
    week = json_data['week']
    # graph 종류
    graphSort = json_data['graphSort']

    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.test
    # $regex :년도 닮음 검색

    find_condition = {key: str(value) for key, value in json_data.items()}
    print('find_condition', find_condition)
    data = collection.find_one(find_condition, projection={"_id": 0}) # objectId 제외
    empty = False
    if data is None:
        empty = True
    data = {'empty': empty, 'plot': data}
    return jsonify({'data':  data})


@app.route('/visual/table/lda', methods=['POST'])
def getLdaTable():
    import pandas as pd
    import numpy as np

    json_data = request.get_json()# 전송한 json data
    print("data 확인", json_data)
    # 년도
    year = json_data['year']
    # 월
    month = json_data['month']

    # 주차
    week = json_data['week']
    # graph 종류
    graphSort = json_data['graphSort']

    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.lda_df_compParts
    # $regex :년도 닮음 검색

    find_condition = {key: str(value) for key, value in json_data.items()}
    print('find_condition', find_condition)
    data = list(collection.find(find_condition,
                                projection={"_id": 0,
                                            'datetime': 1,
                                            "Perc_Contribution": 1,
                                            'category3': 1,
                                            "content": 1
                                            }# objectId 제외
                                )
                )

    # react-bootstrap-table-next를 위한 인조 key 생성
    for index, row in enumerate(data):
        row['key_value'] = index

    # 검색결과 없을 경우
    empty = False
    if data is None:
        empty = True

    data = {'empty': empty, 'product': data}

    return jsonify({'data':  data})


@app.route('/visual/table/model', methods=['POST'])
def getModelTable():
    import pandas as pd
    import numpy as np

    json_data = request.get_json()# 전송한 json data
    print("request confirm", json_data)
    # 년도
    year = json_data['year']
    # 월
    month = json_data['month']
    # 주차
    week = json_data['week']


    client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
    db = client.issue_writer
    collection = db.LSTM_label_compParts
    # $regex :년도 닮음 검색

    find_condition = {key: str(value) for key, value in json_data.items()}
    print('find_condition', find_condition)
    data = list(collection.find(find_condition,
                                projection={"_id": 0,
                                            'datetime': 1,
                                            'label': 1,
                                            'prediction': 1,
                                            'category3': 1,
                                            "content": 1} # objectId 제외
                                )
                )
    # 임시로 데이터 다이어트
    # 데이터는 반드시 하나씩 뽑혀야 합니다.
    print('search result : ', data)
    for index, row in enumerate(data):
        row['key_value'] = index

    # 검색 결과 없을 경우
    empty = False
    if data is None:
        empty = True

    product = data
    data = {'empty': empty, 'product': product}

    return jsonify({'data':  data})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

