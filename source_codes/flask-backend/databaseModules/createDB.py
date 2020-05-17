def createDataBase(cursor):
    cursor.execute("DROP TABLE IF EXISTS Quiz;")
    cursor.execute("DROP TABLE IF EXISTS QuizQ1;")
    cursor.execute("DROP TABLE IF EXISTS QuizQ2;")
    cursor.execute("DROP TABLE IF EXISTS QuizQ3;")
    cursor.execute("DROP TABLE IF EXISTS UserData;")

    create_table_query = ''' CREATE TABLE UserData(
                    Username VARCHAR(255),
                    Password VARCHAR(255),
                    PRIMARY KEY(Username)
                    );'''
    cursor.execute(create_table_query)

    create_table_query = ''' CREATE TABLE QuizQ1(
                    Username VARCHAR(255) REFERENCES UserData(Username),
                    Word VARCHAR(255),
                    Definition TEXT,
                    PRIMARY KEY(Username, Word, Definition)
                    );'''
    cursor.execute(create_table_query)

    create_table_query = ''' CREATE TABLE QuizQ2(
                    Username VARCHAR(255) REFERENCES UserData(Username),
                    Type VARCHAR(255),
                    Word VARCHAR(255),
                    PRIMARY KEY(Username, Type, Word)
                    );'''
    cursor.execute(create_table_query)

    create_table_query = ''' CREATE TABLE QuizQ3(
                    Username VARCHAR(255) REFERENCES UserData(Username),
                    Type VARCHAR(255),
                    Word VARCHAR(255),
                    PRIMARY KEY(Username, Type, Word)
                    );'''

    cursor.execute(create_table_query)
    create_table_query = ''' CREATE TABLE Quiz(
                    QuestionNumber Integer,
                    Username VARCHAR(255) REFERENCES UserData(Username),
                    Type VARCHAR(255),
                    Word VARCHAR(255),
                    PRIMARY KEY(Username, Type, Word)
                    );'''
    cursor.execute(create_table_query)
    
