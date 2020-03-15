import flask 
from modules.Q1FetchData import * 
from flask_cors import CORS
from flask import request 
import requests
import json


app = flask.Flask("__main__")
CORS(app)

@app.route("/", methods=['GET'])
def my_index():
    return "Hello"


@app.route("/api/", methods=['GET'])
def my_api():
    originReact = False
    try: 
        originReact = True
    except: 
        return flask.jsonify({'data':{}})

    if request.method == "GET" and originReact == True:
        dataQ1 = fetchDataQ1("apple",2,5)
        return json.dumps(dataQ1)
  

app.run(debug = True)