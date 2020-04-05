import flask 
from modules.Q1FetchData import * 
from modules.Q2FetchData import * 
from modules.Q3FetchData import * 
from graphCreation.main import *
from flask_cors import CORS
from flask import request 
import requests
import json
import time 
import os 


app = flask.Flask("__main__")
CORS(app)
 

def eraiseContent():
    open("Q1.txt", 'w').close()
    open("Q2.txt", 'w').close()
    open("Q3.txt", 'w').close()


@app.route("/", methods=['GET','POST'])
def my_index():
    if request.method == "POST":
        eraiseContent()

        data = request.data.decode('utf8').replace("'", '"')
        data = json.loads(data)
        word = data["d"]
        generateGraph(word,[[1,5],[2,2],[3,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,50],[2,10],[-2,10]])
        print("Generated")
        dataQ1 = fetchDataQ1(word,2,5)
        dataQ2 = createQuestion2Words(word, 2,2, 5, 12)
        dataQ3 = createQuestion3Words(word, 2, 12)

        with open("Q1.txt","w") as outfile: 
            json.dump(dataQ1,outfile)

        with open("Q2.txt","w") as outfile: 
            json.dump(dataQ2,outfile)

        with open("Q3.txt","w") as outfile: 
            json.dump(dataQ3,outfile)

        print("Graph and quiz are created")
        created = True 

        return "finished"
    
    if request.method == "GET":
        return {"d": "finished"}


@app.route("/Q1", methods=['GET','POST'])
def q1():
    with open('Q1.txt') as json_file:
        return json.load(json_file)
  
@app.route("/Q2", methods=['GET','POST'])
def q2():
    with open('Q2.txt') as json_file:
        return json.load(json_file)

@app.route("/Q3", methods=['GET','POST'])
def q3():
    with open('Q3.txt') as json_file:
        return json.load(json_file)

app.run(debug = True, threaded=False)