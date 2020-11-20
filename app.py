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

import json
import datetime
from json import JSONEncoder

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

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


@app.route('/company_profile')
def company_profile():
    name = request.args.get('name')
    A = list(dev.aggregate([{'$match' : {'CompanyName': name}},
                        {'$group' : {
                            '_id': '$Indication',
                            'count': {'$sum': 1}
                        }}]))
    drugs = sorted(A, key=lambda current: current['count'], reverse=True)[:10]

    holder = {}
    holder['chart'] = [{'label': x['_id'], 'y':x['count']} for x in drugs]
    holder['pipeline'] =  list(dev.aggregate([{'$match' : {'CompanyName': name}}, {'$sort': {'StatusDate': 1}},
                {'$group': 
                          {'_id':{'DrugName':'$DrugName', 'Indication':'$Indication'},
                           'lastUpdate': {'$last': '$StatusDate'},
                           'lastPhase': {'$last': '$DevelopmentStatus'}
                           }

                 }]))

    return Response(json.dumps(holder, indent=4, cls=DateTimeEncoder),  mimetype='application/json')


@app.route('/pipeline_data')
def pipeline_data():
    name = request.args.get('name')
    data = list(dev.aggregate([{'$match' : {'CompanyName': 'Prevail Therapeutics Inc'}}, {'$sort': {'StatusDate': 1}},
                {'$group': 
                          {'_id':{'DrugName':'$DrugName', 'Indication':'$Indication'},
                           'lastUpdate': {'$last': '$StatusDate'},
                           'lastPhase': {'$last': '$DevelopmentStatus'}
                           }

                 }]))
    return Response(json.dumps(data, indent=4, cls=DateTimeEncoder),  mimetype='application/json')




print('made it here')


if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5000, debug = True) 