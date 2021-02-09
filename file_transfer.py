from flask import Flask, request, jsonify
from bokeh.embed import json_item
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False;

@app.route('/visual', methods=['POST'])
def getVariableAndPutBokeh():

    """
    :param YearweekNum: 년도+주차숫자
    :return: 통계시각화데이터
    """
    json_data = request.get_json()# 전송한 json data
    print("data 확인",json_data)
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
    collection = db.visual_data
    # $regex :년도 닮음 검색

    find_condition = {key: str(value) for key, value in json_data.items()}
    print('find_condition', find_condition)
    data = list(collection.find(find_condition,
                                projection={"_id": 0} # objectId 제외
                                )
                )
    # 임시로 데이터 다이어트
    # 데이터는 반드시 하나씩 뽑혀야 합니다.

    if data != []:
        data = data[0]
    else:
        data = list(collection.find({"graph_sort": graphSort},
                                projection={"_id": 0}  # objectId 제외
                                )
                    # .sort({"year":  1#,
                    #                    # "month": 1,
                    #                    # "week":  1
                    #                    }
                    #                    ).limit(1)
                    )[0]


    return jsonify({'data':  data})


@app.route('/visual/table/lda', methods=['POST'])
def getLdaTable():
    import pandas as pd
    import numpy as np

    json_data = request.get_json()# 전송한 json data
    print("data 확인",json_data)
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
                                            "content": 1} # objectId 제외
                                )
                )
    # 임시로 데이터 다이어트
    # 데이터는 반드시 하나씩 뽑혀야 합니다.
    if data == []:
        data = list(collection.find({},
                                projection={"_id": 0,
                                            'datetime': 1,
                                            "Perc_Contribution": 1,
                                            'category3': 1,
                                            "content": 1}  # objectId 제외
                                )
                    # .sort({"year":  1#,
                    #                    # "month": 1,
                    #                    # "week":  1
                    #                    }
                    #                    ).limit(1)
                    )

    print(data)
    for index, row in enumerate(data):
        row['key_value'] = index
    column_list = ['Perc_Contrigution', 'datetime','category3','Dominant_topic','content']
    product = data
    data = {'column': column_list, 'product': product}
    print('table')
    # column 구조
    # [{dataField : 'id',text: "Product ID}]

    # data 구조
    # [[row1],[row2],[row3]]

    return jsonify({'data':  data})


@app.route('/visual/table/model', methods=['POST'])
def getModelTable():
    import pandas as pd
    import numpy as np

    json_data = request.get_json()# 전송한 json data
    print("data 확인",json_data)
    # 년도
    year = json_data['year']
    # 월
    month = json_data['month']

    # 주차
    week = json_data['week']
    # graph 종류


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
    if data == []:
        data = list(collection.find({"difference": True},
                                projection={"_id": 0,
                                            'datetime': 1,
                                            'label': 1,
                                            'prediction': 1,
                                            'category3': 1,
                                            "content": 1}   # objectId 제외
                                ).limit(30)
                    # .sort({"year":  1#,
                    #                    # "month": 1,
                    #                    # "week":  1
                    #                    }
                    #                    ).limit(1)
                    )

    print(data)
    for index, row in enumerate(data):
        row['key_value'] = index
    column_list = ['datetime', 'label','prediction', 'content']
    product = data
    data = {'column': column_list, 'product': product}
    print('table')
    print(product[0].keys())
    # column 구조
    # [{dataField : 'id',text: "Product ID}]

    # data 구조
    # [[row1],[row2],[row3]]

    return jsonify({'data':  data})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

