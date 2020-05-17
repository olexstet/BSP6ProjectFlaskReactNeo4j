import random 

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

def jsonToDBQ1(id_quiz, id_question, word, data, points, cursor, connection):
    dataShuffled = [] 
    index = 1
    for w in data:
        definition = data[w]
        dataShuffled.append((index, definition))
        index += 1

    random.shuffle(dataShuffled)

    questionData = "{"
    for i in range(len(dataShuffled)):
        _,definition = dataShuffled[i]
        if i != len(dataShuffled)-1:
            questionData += checkDefinition(definition)+","
        else:
            questionData += checkDefinition(definition)+"}"

    correctPos = "{"
    print(dataShuffled)
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i]
        if pos == 1: 
            correctPos += str(i)+"}"

    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")"
    cursor.execute(query)
    connection.commit()
    print("done")


def jsonToDBQ2(id_quiz, id_question,data, points, cursor, connection):
    dataShuffled = [] 
    array = []
    count = 0
    for w in data:
        if count == 0:
            word = w
            count = 1
        array += data[w]
    
    print(array)
    numberCorrect = len(data[word])-1

    for i in range(len(array)):
        dataShuffled.append((i,array[i]))

    random.shuffle(dataShuffled)

    questionData = "{"
    for i in range(len(dataShuffled)):
        _,w = dataShuffled[i]
        w = apostropheWord(w)
        if i != len(dataShuffled)-1:
            questionData += w+","
        else:
            questionData += w+"}"

    correctPos = "{"
    print(questionData)
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i]
        if pos <= numberCorrect: 
            if i != len(dataShuffled)-1:
                correctPos += str(i)+","
    correctPos = correctPos[:len(correctPos)-1] 
    correctPos += "}"

    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")"
    cursor.execute(query)
    connection.commit()
    print("done")

def jsonToDBQ3(id_quiz, id_question,data, points, cursor, connection):
    dataShuffled = [] 
    array = []
    count = 0
    for w in data:
        if count == 0:
            word = w
            count = 1
        array += data[w]
    
    print(array)
    numberCorrect = len(data[word])-1

    for i in range(len(array)):
        dataShuffled.append((i,array[i]))

    random.shuffle(dataShuffled)

    questionData = "{"
    for i in range(len(dataShuffled)):
        _,w = dataShuffled[i]
        w = apostropheWord(w)
        if i != len(dataShuffled)-1:
            questionData += w+","
        else:
            questionData += w+"}"

    correctPos = "{"
    print(questionData)
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i]
        if pos <= numberCorrect: 
            if i != len(dataShuffled)-1:
                correctPos += str(i)+","
    correctPos = correctPos[:len(correctPos)-1] 
    correctPos += "}"

    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")"
    cursor.execute(query)
    connection.commit()
    print("done")
