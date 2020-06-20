import sys 
sys.path.insert(0, '..\..\env\Lib\site-packages') # if psycopg2 doesn't work 
import psycopg2
    
def createDataBase(cursor): # structure of database 
    cursor.execute("DROP TABLE IF EXISTS Answer;")
    cursor.execute("DROP TABLE IF EXISTS Question;")
    cursor.execute("DROP TABLE IF EXISTS Questions;")
    cursor.execute("DROP TABLE IF EXISTS Quizzes;")
    cursor.execute("DROP TABLE IF EXISTS Account;")


    create_table_query = '''CREATE TABLE Account(
                            Username VARCHAR(255) UNIQUE,
                            Password VARCHAR(255) Unique, 
                            PRIMARY KEY(Username, password) 
                        );'''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE Quizzes(
                            Username VARCHAR(255) UNIQUE REFERENCES Account(Username),
                            QuizId INTEGER Unique, 
                            Status VARCHAR(255),
                            PRIMARY KEY(Username, QuizId)
                            );'''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE Question(
                            QuizId INTEGER REFERENCES Quizzes(QuizId),
                            QuestionId INTEGER UNIQUE,
                            Word Varchar(255),
                            QuestionData TEXT[],
                            CorrectPos Integer[],
                            QuestionPoints Integer,
                            PRIMARY KEY(QuizId, QuestionId)
                            );'''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE Answer(
                            QuestionId INTEGER REFERENCES Question(QuestionId) UNIQUE,
                            CorrectPos Integer[],
                            AnswerPos Integer[],
                            NumberCorrect Integer,
                            GradeQuestion Integer,
                            UNIQUE(QuestionId),
                            PRIMARY KEY(QuestionId)
                            );'''
    cursor.execute(create_table_query)

def getDBCursor(): # fetch a cursor pointed to database 
    hostname = '127.0.0.1'
    username = 'postgres' # username in database 
    passwordDB = '****' # please change/eneter the password 
    databaseName = 'webApp' # name of database in PostgreSQL 
    connection = psycopg2.connect("dbname = "+databaseName+" user = "+username+" password = "+passwordDB+" host = localhost")
    cursor = connection.cursor()
    return cursor, connection

def createDB():
    cursor, connection = getDBCursor() # fetch cursor 
    createDataBase(cursor) # create new database 
    cursor.execute("""Insert Into Account VALUES('admin', 'admin')""") # add initial user admin 
    cursor.close() #  close cursor 
    connection.commit() # save changes 
    connection.close() 
    print("Database Created")
