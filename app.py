from flask import Flask
from flask_cors import CORS
from flask import jsonify
from pymongo import MongoClient
from flask import request


client = MongoClient('mongodb://david:cis400@157.230.216.187:27017')
db = client.pipeline
dev = db.trails

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    search = request.args.get('search')
    print(search)
    return jsonify(list(dev.distinct( "DrugName", {"DrugName" : {'$regex':  f'^{search}.*' }} ))[:10])


print('made it here')


if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5000, debug = True) 