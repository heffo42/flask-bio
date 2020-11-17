from flask import Flask
from flask_cors import CORS
from flask import jsonify
from pymongo import MongoClient
from flask import request
from flask import Response
import json


client = MongoClient('mongodb://david:cis400@157.230.216.187:27017')
db = client.pipeline
dev = db.trails

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    search = request.args.get('search')
    print(search)
    return jsonify(list(dev.distinct( "DrugName", {"DrugName" : {'$regex':  f'^{search}.*','$options':  'i' }} ))[:10])

@app.route('/company')
def company_search():
    search = request.args.get('search')
    print(search)
    return jsonify(list(dev.distinct( "CompanyName", {"CompanyName" : {'$regex':  f'^{search}.*', '$options':  'i'}} ))[:10])


@app.route('/details')
def get_drug_details():
    drug_name = request.args.get('drug_name')
    print(f'drug name {drug_name}')
    x = list(dev.find({'DrugName': drug_name},  {'_id': 0}))
    return Response(json.dumps(x),  mimetype='application/json')

@app.route('/coco')
def coco():
    return jsonify('hi coco')




print('made it here')


if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5000, debug = True) 