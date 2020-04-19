import flask 
from generators.Q1FetchData import * 
from generators.Q2FetchData import * 
from generators.Q3FetchData import * 
from graphCreation.main import *
from flask_cors import CORS
from flask import request 
import requests
import json
import time 
import os 
from databaseModules.createDB import *
from databaseModules.jsonToDB import *

sys.path.insert(0, '..\env\Lib\site-packages') # if psycopg2 doesn't work 
import psycopg2


app = flask.Flask("__main__")
CORS(app)


def getDBCursor():
    hostname = '127.0.0.1'
    username = 'postgres'
    passwordDB = 'Sasha!stet!1998'
    databaseName = 'webApp'
    connection = psycopg2.connect("dbname = "+databaseName+" user = "+username+" password = "+passwordDB+" host = localhost")
    cursor = connection.cursor()
    return cursor, connection

def createDB():
    cursor, connection = getDBCursor()
    createDataBase(cursor)
    cursor.execute("""Insert Into UserData Values('admin', 'admin')""") # to be remove 
    cursor.close()
    connection.commit()
    connection.close()
    print("Database Created")


@app.route("/", methods=['GET','POST'])
def my_index():
    print(request)
    data = request.data.decode('utf8').replace("'", '"')
    data = json.loads(data)
    print(data["typeRequest"])

    if request.method == "POST" and data["typeRequest"] == "Login":
        username = data['dataLogin']['username']
        password = data['dataLogin']['password']
        print(username, password)
        cursor, connection = getDBCursor()
        query = """ Select Username, Password FROM UserData Where Username = '"""+username+"""' and Password = '"""+ password +"""'"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        if len(result) == 1:
            return 'Exists'
        else:
            return 'Not Exists'
        

    if request.method == "POST" and data["typeRequest"] == "create_quiz":

        word = data["d"]["currentTerm"]
        username = data["d"]["username"]

        generateGraph(word,[[1,5],[2,2],[3,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,50],[2,10],[-2,10]])
        print("Graph Generated")
        print("Start Generating Questions For Quiz")
        dataQ1 = fetchDataQ1(word,2,5)
        dataQ2 = createQuestion2Words(word, 2,2, 5, 12)
        dataQ3 = createQuestion3Words(word, 2, 12)

        print(dataQ2)

        cursor, connection = getDBCursor()
        jsonToDBQ1(dataQ1, username, cursor, connection)
        jsonToDBQ2(dataQ2, username, cursor, connection)
        jsonToDBQ3(dataQ3, username, cursor, connection)
    
        cursor.close()
        connection.commit()
        connection.close()

        print("Graph and quiz are created")
        return "finished"
    
    if request.method == "POST" and data["typeRequest"] == "Q1":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select word, definition FROM QuizQ1 Where Username = '"""+username+"""'"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        dataQ1 = {}
        for word,definition in result:
            dataQ1[word] = definition
        return dataQ1

    if request.method == "POST" and data["typeRequest"] == "Q2":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select Type FROM QuizQ2 Where Username = '"""+username+"""'"""
        cursor.execute(query)
        categories = cursor.fetchall()
        categories = set(categories)
        
        dataQ2 = {}
        for category in categories:
            query = """ Select Word FROM QuizQ2 Where Username = '""" +username+ """' and Type = '""" +category[0]+"""'""" 
            cursor.execute(query)
            categories = cursor.fetchall()
            dataQ2[category[0]] = categories

        cursor.close()
        connection.commit()
        connection.close()
        return dataQ2

    if request.method == "POST" and data["typeRequest"] == "Q3":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select Type FROM QuizQ3 Where Username = '"""+username+"""'"""
        cursor.execute(query)
        categories = cursor.fetchall()
        categories = set(categories)
        
        dataQ3 = {}
        for category in categories:
            query = """ Select Word FROM QuizQ3 Where Username = '""" +username+ """' and Type = '""" +category[0]+"""'""" 
            cursor.execute(query)
            categories = cursor.fetchall()
            dataQ3[category[0]] = categories

        cursor.close()
        connection.commit()
        connection.close()
        return dataQ3

if __name__ == "__main__":
    createDB()
    app.run(debug = True, threaded=True)
