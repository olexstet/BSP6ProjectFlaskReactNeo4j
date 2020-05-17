import flask 
from generators.Q1FetchData import * 
from generators.Q2FetchData import * 
from generators.Q3FetchData import * 
from graphCreation.graphCreate import *
from flask_cors import CORS
from flask import request 
import requests
import json
import time 
import os 
from databaseModules.databaseManagement import *
from databaseModules.jsonToDB import *


app = flask.Flask("__main__")
CORS(app)

id_quiz = 1
id_question = 1 

@app.route("/", methods=['GET','POST'])
def my_index():
    global id_quiz 
    global id_question 

    data = request.data.decode('utf8').replace("'", '"')
    data = json.loads(data)

    if request.method == "POST" and data["typeRequest"] == "Login":
        username = data['dataLogin']['username']
        password = data['dataLogin']['password']
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

        #----------- Create a new quiz in database----------------------------
        cursor, connection = getDBCursor()
        query = """ INSERT INTO Quizzes VALUES("""+"'"+username+"',"+str(id_quiz)+""", 'IN PROGRESS')"""
        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()

        #----------- Generate Data for questions -----------------------------

        generateGraph(word,[[1,5],[2,2],[3,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,50],[2,10],[-2,10]])
        print("Graph Generated")
        print("Start Generating Questions For Quiz")
        dataQ1 = fetchDataQ1(word,2,5)
        print(dataQ1)
        dataQ2 = createQuestion2Words(word, 2,2, 5, 12)
        dataQ3 = createQuestion3Words(word, 2, 12)

        print(dataQ2)
        print(dataQ3)

        cursor, connection = getDBCursor()
        jsonToDBQ1(id_quiz,id_question,word,dataQ1,5, cursor, connection)
        id_question += 1
        jsonToDBQ2(id_quiz,id_question,dataQ2,5, cursor, connection)
        id_question += 1
        jsonToDBQ3(id_quiz,id_question,dataQ3,5, cursor, connection)
        id_question = 1
        id_quiz += 1

        cursor.close()
        connection.commit()
        connection.close()

        print("Graph and quiz are created")
        return "finished"
    
    if request.method == "POST" and data["typeRequest"] == "Q1":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select quizId FROM Quizzes Where Username = '"""+username+"""' ORDER BY quizId DESC LIMIT 1"""
        cursor.execute(query)
        idQuiz = cursor.fetchall()[0][0]

        query = """ Select questionData FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(1)
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        cursor.close()
        connection.close()
        dataQ1 = {}
        index = 1
        for definition in result:
            dataQ1[index] = definition
            index += 1
        return dataQ1

    if request.method == "POST" and data["typeRequest"] == "Q2":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select quizId FROM Quizzes Where Username = '"""+username+"""' ORDER BY quizId DESC LIMIT 1"""
        cursor.execute(query)
        idQuiz = cursor.fetchall()[0][0]

        query = """Select word, correctPos FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(2)
        cursor.execute(query)
        result = cursor.fetchall()[0]
        category = result[0]
        correctPos = result[1]
        
        dataQ2 = {}
        query = """ Select questionData FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(2)
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        correct = []
        false = []
        for i in range(len(result)):
            if i in correctPos:
                correct.append(result[i])
            else:
                false.append(result[i])
        dataQ2[category] = correct
        dataQ2['random'] = false

        cursor.close()
        connection.commit()
        connection.close()
        return dataQ2

    if request.method == "POST" and data["typeRequest"] == "Q3":
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select quizId FROM Quizzes Where Username = '"""+username+"""' ORDER BY quizId DESC LIMIT 1"""
        cursor.execute(query)
        idQuiz = cursor.fetchall()[0][0]

        query = """Select word, correctPos FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(3)
        cursor.execute(query)
        result = cursor.fetchall()[0]
        category = result[0]
        correctPos = result[1]
        
        dataQ2 = {}
        query = """ Select questionData FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(3)
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        correct = []
        false = []
        for i in range(len(result)):
            if i in correctPos:
                correct.append(result[i])
            else:
                false.append(result[i])
        dataQ2[category] = correct
        dataQ2['random'] = false

        cursor.close()
        connection.commit()
        connection.close()
        return dataQ2

if __name__ == "__main__":
    createDB()
    app.run(debug = True, threaded=True)
