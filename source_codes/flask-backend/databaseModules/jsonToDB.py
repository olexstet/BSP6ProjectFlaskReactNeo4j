import random 

def apostropheWord(word): # adapt a word for stroing to database 
    res = ""
    for char in word:
        if char == "'":
            res += "\'"+"'" # adaptation in case of aposthrophe 
        else:
            res += char
    return res 

def checkDefinition(definition): # check if in definition an aposthrophe is present and adapt to the needed format 
    res = ""
    definition = definition.split(" ")
    for word in definition: 
        if "'" in word: 
            w = apostropheWord(word) # adaptation 
        else:
            w = word
        res += w+" "
    return res 

def jsonToDBQ1(id_quiz, id_question, word, data, points, cursor, connection): # store the data for question 1 
    dataShuffled = [] 
    index = 1
    for w in data:
        definition = data[w] # fetch definitions 
        dataShuffled.append((index, definition)) # store the definition to shuflle 
        index += 1

    random.shuffle(dataShuffled) # shuffle definitons 

    questionData = "{" 
    for i in range(len(dataShuffled)): # put together the data as a string in brackets for adapting to the database format  
        _,definition = dataShuffled[i]
        if i != len(dataShuffled)-1:
            questionData += checkDefinition(definition)+","
        else:
            questionData += checkDefinition(definition)+"}"

    correctPos = "{" # pos of correct definition 
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i] # fetch position 
        if pos == 1: # if it is the first position then the definition is correct. Initally the right definition was at first position. 
            correctPos += str(i)+"}"

   
    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")" # store into database 
    cursor.execute(query)
    connection.commit()
    print("Q1 done")


def jsonToDBQ2(id_quiz, id_question,data, points, cursor, connection):
    dataShuffled = [] 
    array = []
    count = 0
    for w in data:
        if count == 0:
            word = w # fetch the category 
            count = 1
        array += data[w]
    
    numberCorrect = len(data[word])-1 # how much words are correct 

    for i in range(len(array)):
        dataShuffled.append((i,array[i])) # append the words to array to shuffle 

    random.shuffle(dataShuffled) # shuffle array 

    questionData = "{"
    for i in range(len(dataShuffled)):
        _,w = dataShuffled[i]
        w = apostropheWord(w) # check if word has aposthrophe 
        if i != len(dataShuffled)-1:
            questionData += w+","
        else:
            questionData += w+"}"

    correctPos = "{"

    # find the position of words whoch are correct 
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i]
        if pos <= numberCorrect: 
            if i != len(dataShuffled)-1:
                correctPos += str(i)+","
    if len(correctPos) > 1:
        correctPos = correctPos[:len(correctPos)-1] 
    correctPos += "}"

    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")"
    cursor.execute(query)
    connection.commit()
    print("Q2 done")

def jsonToDBQ3(id_quiz, id_question,data, points, cursor, connection): # same as previous function 
    dataShuffled = [] 
    array = []
    count = 0
    for w in data:
        if count == 0:
            word = w
            count = 1
        array += data[w]
    
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
    for i in range(len(dataShuffled)):
        pos,_ = dataShuffled[i]
        if pos <= numberCorrect: 
            if i != len(dataShuffled)-1:
                correctPos += str(i)+","
            else:
                correctPos += str(i)
    if len(correctPos) > 1:
        correctPos = correctPos[:len(correctPos)-1] 
    correctPos += "}"

    query = " INSERT INTO Question VALUES(" + str(id_quiz) + "," + str(id_question)+"," +"'"+ str(word)+"','" + questionData + "','"+correctPos+"',"+str(points)+")"
    cursor.execute(query)
    connection.commit()
    print("Q3 done")

