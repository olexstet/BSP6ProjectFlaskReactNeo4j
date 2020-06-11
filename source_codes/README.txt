This folder contains all the codes written for the Bachelor Semester Project S6 & S4.
You can find three folders (env, flask-backend and frontend).

Summary of folders: 

env folder (outside for some reasons): 
It is a virtual environment folder which contains all the libraries used in this project. 

flask-backend folder: 
It contains the codes wrote in Python programming language which represent the server side dedicated to handle and process 
the requests from the front-end. The server is based on Flask framework dedicated to web development. 
His first purpose is to generate quizzes based on a word by using generators which can be find inside in the
'generators' folder. The goal of each generator is to provide the data for a multiple choice question based on a 
graph database(Neo4j). The code for the creation of a graph in a graph database can be find in 'graphCreation' folder. 
Additionaly, the server uses a relational database (PostgreSQL) for which the code can be find in the 'databaseModules' folder. 
For testing how the graph is working, a python notebook can be run (if Neo4j database is running)

frontend folder:
The front-end is based on React framework which allows the development of front-end. The front-end side is composed of 
three folders (node_modules, public and src). Node_modules contains diffetent libraries used during the front-end development
and the public folder contains the index.html file which represent the we page. 
The most important folder is 'src' folder which is used for development.
Composition: 
	- components: pieces of 'objects' or parts used in different pages. As example checkBox, question section, etc.
	- pages: are different pages of the front-end which are used for interaction between server and end-users 
	- App.js: is the basic JavaScript file which is compose of link for pages and also allow to dsplay a page. 

How it works? 

Prerequisites and Installation: 

Neo4j: 
1) Install a Neo4j Database on our computer. 
2) Create a project
3) Createa graph 
4) Start the server of the graph. 
5) Open browser and check the connection. It should be bolt://localhost:7687 

PostgreSQL: 
I use phAdmin 4 for manipulating the database. 
1) Install PostgreSQL 
2) Create a database, I use 'webApp' name 

Changes in the code: 
Neo4j: 
1) Go in source_codes folder/flask-beackend/graphCreation/graphSetups/commands
2) Change connect() function by setting first the localhost of our database (if not the same) and modify auth (username, password) 

PostgreSQL: 
1) Go in source_codes folder/flask-beackend/databaseModules/databaseManagement
2) In getDBCursor() function replace the personal data for connecting to database by our hostname, username and password (passwordDB)

Npm: 
- Install npm 

Runnning codes: 
1) Open two terminal and navigate into the folder which contains env folder. (1 terminal for back-end and 1 for front-end)
2) Connect to virtual environment. This is the 'env' folder. For connection, I use .\env\Scripts\activate (only in 1 terminal)
Remark: If you have the problem with the env folder because you have the libraries not installed, install them by using requirements freeze. 
3) Go into our terminal where you have environment activated and access the 'flask-backend' folder (use cd if windows)
4) Inside run 'python main.py' and normally the server should start 
5) Let the server running 
6) Go into the second terminal and navigate to frontend (cd frontend) and run npm.start and the front-end should appear. 

Navigate in the software: 
1) Enter 'admin' as username and password 
2) Choose a word, we work on word 'apple', click do quiz 
3) A waiting window will appear, in the server console you can see that a creation of the graph is in process. 
4) Click Ready when it appears and you will be redirected to the quiz 
5) Unfortunatly, the 'Submit' button doesn't work at least yet and the comeBack doesn't work, a fix will come soon. 
6) For trying another graph restart the server 'python main.py' and access the url localhost:3000/
