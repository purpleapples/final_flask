from flask import Flask, request, jsonify
from bokeh.embed import json_item
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

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

@app.route('/visual/table', methods=['POST'])
def getInfoTable():
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
    collection = db.lda_df_compParts
    # $regex :년도 닮음 검색

    find_condition = {key: str(value) for key, value in json_data.items()}
    print('find_condition', find_condition)
    data = list(collection.find(find_condition,
                                projection={"_id": 0}  # objectId 제외
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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

