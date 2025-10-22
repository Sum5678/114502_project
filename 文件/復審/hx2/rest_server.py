'''
rest_server.py
version: 2.3  @2023/05/01
Wenchin Hsieh @Goomo.Net Studio, wenchin@goomo.net
'''

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 初始資料
database = {'apple': 5, 'banana': 3, 'orange': 2}


# 查詢全部資料
@app.route('/fruit/read_all', methods=['GET'])
def read_collection():
    app.logger.info("read_collection()")
    return jsonify(database)


# 查詢單筆資料 (方法一: by URL Path)
@app.route('/fruit/read/<string:key>', methods=['GET'])
def read_docu_path(key):
    app.logger.info("read_docu_path('%s') by URL Path.", key)
    if key in database:
        return jsonify({key: database[key]})
    else:
        return jsonify({'result': 'data not found'})


# 查詢單筆資料 (方法二: by Argument)
@app.route('/fruit/read', methods=['GET'])
def read_docu_arg():
    key = request.args.get('key')
    app.logger.info("read_docu_arg() by Argument: 'key=%s'", key)
    if key in database:
        return jsonify({key: database[key]})
    else:
        return jsonify({'result': 'data not found'})


# 新增資料 (by Request Body)
@app.route('/fruit/create', methods=['POST'])
def create_docu():
    docu = request.get_json()
    app.logger.info("create_docu() by Request Body: %s", docu)
    name = docu['name']
    amount = docu['amount']
    database[name] = amount
    return jsonify({'result': 'inserted successfully'})


# 刪除資料 (方法一: by URL Path)
@app.route('/fruit/delete/<string:key>', methods=['DELETE'])
def delete_docu_path(key):
    app.logger.info("delete_docu_path('%s') by URL Path.", key)
    if key in database:
        del database[key]
        return jsonify({'result': 'deleted successfully'})
    else:
        return jsonify({'result': 'data not found'})


# 刪除資料 (方法二: by Request Body)
@app.route('/fruit/delete', methods=['DELETE'])
def delete_docu():
    docu = request.get_json()
    app.logger.info("delete_docu() by Request Body: %s", docu)
    key = docu['key']
    if key in database:
        del database[key]
        return jsonify({'result': 'deleted successfully'})
    else:
        return jsonify({'result': 'data not found'})


# 修改資料 (by URL Path)
@app.route('/fruit/replace/<string:key>', methods=['PUT'])
def replace_docu_path(key):
    docu = request.get_json()
    app.logger.info("replace_docu_path('%s') by URL Path: %s", key, docu)
    if key in database:
        name = docu['name']
        amount = docu['amount']
        if key != name:
            del database[key]
        database[name] = amount
        return jsonify({'result': 'replaced successfully'})
    else:
        return jsonify({'result': 'data not found'})


# 主程式
if __name__ == '__main__':
    app.run(debug=True)