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


app = flask.Flask("__main__") # create application 
CORS(app)

id_quiz = 1 # id for quizzes 
id_question = 1  # id for questions 

@app.route("/", methods=['GET','POST'])
def my_index():
    global id_quiz 
    global id_question 

    data = request.data.decode('utf8').replace("'", '"') #receive data and convert to json 
    data = json.loads(data)

    if request.method == "POST" and data["typeRequest"] == "Login": # Login request response 
        username = data['dataLogin']['username'] # username 
        password = data['dataLogin']['password'] # password 
        cursor, connection = getDBCursor() # connect to database 
        query = """ Select Username, Password FROM UserData Where Username = '"""+username+"""' and Password = '"""+ password +"""'""" # fetch user with the same username and password 
        cursor.execute(query)
        result = cursor.fetchall() # fetch result of query 
        cursor.close()
        connection.commit()
        connection.close()
        if len(result) == 1: # if exists 
            return 'Exists'
        else:
            return 'Not Exists'

    if request.method == "POST" and data["typeRequest"] == "Check_Term": # check existance of a requested term
        term = data['dataCheck']['term'] # term 
        check_result = check_term_existance(term) # verification function 
        if check_result == True: # term exists in wordNet 
            return "Exists"
        else:   
            return "Not Exists"
        

    if request.method == "POST" and data["typeRequest"] == "create_quiz": # Request for quiz creation 

        word = data["d"]["currentTerm"] # term 
        username = data["d"]["username"] # username 

        #----------- Create a new quiz in database----------------------------
        cursor, connection = getDBCursor()
        query = """ INSERT INTO Quizzes VALUES("""+"'"+username+"',"+str(id_quiz)+""", 'IN PROGRESS')"""
        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()

        #----------- Generate Data for questions -----------------------------

        generateGraph(word,[[1,5],[2,2],[3,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,50],[2,10],[-2,10]]) # graph creation 
        print("Graph Generated")
        print("Start Generating Questions For Quiz")
        dataQ1 = fetchDataQ1(word,2,5) # generator 1 
        
        dataQ2 = createQuestion2Words(word, 2,2, 12) # generator 2 
        dataQ3 = createQuestion3Words(word, 2, 12) # generator 3 

        #------------ Store questions data in database -------------------------
        cursor, connection = getDBCursor()
        jsonToDBQ1(id_quiz,id_question,word,dataQ1,5, cursor, connection) 
        id_question += 1 # increase question id 
        jsonToDBQ2(id_quiz,id_question,dataQ2,5, cursor, connection)
        id_question += 1
        jsonToDBQ3(id_quiz,id_question,dataQ3,5, cursor, connection)
        id_question = 1 # set id for next question 
        id_quiz += 1 # increase quiz id 

        cursor.close()
        connection.commit()
        connection.close()

        print("Graph and quiz are created")
        return "finished"
    
    if request.method == "POST" and data["typeRequest"] == "Q1": # Request for data fro question 1 
        username = data["username"]
        cursor, connection = getDBCursor()
        query = """ Select quizId FROM Quizzes Where Username = '"""+username+"""' ORDER BY quizId DESC LIMIT 1""" # select last quiz 
        cursor.execute(query)
        idQuiz = cursor.fetchall()[0][0]

        query = """ Select questionData FROM Question Where quizId = """+str(idQuiz)+""" and questionId = """+str(1) # select question with id 1 
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        cursor.close()
        connection.close()
        dataQ1 = {}
        index = 1
        for definition in result: # put definitions into dictionary 
            dataQ1[index] = definition
            index += 1
        return dataQ1

    if request.method == "POST" and data["typeRequest"] == "Q2": # Request for data of question 2 
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
        # fetch correct and random words 
        for i in range(len(result)):
            if i in correctPos:
                correct.append(result[i])
            else:
                false.append(result[i])
        # put in dictionary 
        dataQ2[category] = correct
        dataQ2['random'] = false

        cursor.close()
        connection.commit()
        connection.close()
        return dataQ2

    if request.method == "POST" and data["typeRequest"] == "Q3": # same as previous request 
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
    createDB() # create database 
    app.run(debug = True, threaded=True)
