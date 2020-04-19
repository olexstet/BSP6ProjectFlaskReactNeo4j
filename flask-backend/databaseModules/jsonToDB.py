def apostropheWord(word):
    res = ""
    for char in word:
        if char == "'":
            res += "''"
        else:
            res += char
    return res 

def checkDefinition(definition):
    res = ""
    definition = definition.split(" ")
    for word in definition: 
        if "'" in word: 
            w = apostropheWord(word)
        else:
            w = word
        res += word+" "
    return res 

def jsonToDBQ1(data, username, cursor, connection):
    for word in data:
        query = """INSERT INTO QuizQ1 VALUES('""" + username +"""','""" + word + """','""" + checkDefinition(data[word]) +"""')"""
        cursor.execute(query)
    connection.commit()


def jsonToDBQ2(data, username, cursor, connection):
    for key in data:
        for word in data[key]:
            w = word
            if "'" in word: 
                w = apostropheWord(word)

            query = """INSERT INTO QuizQ2 VALUES('""" + username +"""','""" + key + """','""" + w +"""')"""
            cursor.execute(query)
    connection.commit()

def jsonToDBQ3(data, username, cursor, connection):
    for key in data:
        for word in data[key]:
            w = word
            if "'" in word: 
                w = apostropheWord(word)

            query = """INSERT INTO QuizQ3 VALUES('""" + username +"""','""" + key + """','""" + w +"""')"""
            cursor.execute(query)
    connection.commit()