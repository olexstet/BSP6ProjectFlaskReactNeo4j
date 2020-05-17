from graphCreation.convertSynsetToString import *
from nltk.corpus import wordnet as wn

def generateLabel(labelSequence, separation):
    result = ""
    for i in range(len(labelSequence)):
        element = labelSequence[i]
        if i != len(labelSequence)-1:
            result += element + separation
        else:
            result += element 
    return result

def addToFile(string):
    f = open("graphCreation/cypherScript.txt", "r")
    saveD = f.read()
    f.close()
    f = open("graphCreation/cypherScript.txt", "w")
    f.write(saveD)
    f.write(string+"\n")
    f.close()

def createNode(S,graph):
    result = convertHypernymsToString([S])
    defType = {"n": "Name", "v": "Verbe", "a": "Adjective", "r": "Adverbe"}

    w = result[0]

    typeW = S.pos()
    typeW = defType[typeW]

    label = generateLabel([w,typeW], "::")

    definition = wn.synsets(w)[0].definition()
    definition = definition.replace('"','')

    query = "Match (t:Term) return t"

    countNodes = 0
    nodes = graph.run(query)
    names =[]
    for node in nodes:
        names.append(node[0]['name'])
    #print(names)

    if w in names:
        countNodes += 1
        
    if countNodes == 0:
        query = 'MERGE (t:Term {name: '+'"'+w+'", definition: "'+ definition + '" , type: "'+typeW+'" , label: "'+label+'" })'
        string = str('MERGE (t:Term {name: '+'"'+w+'", definition: "'+ definition + '" , type: "'+typeW+'" , label: "'+label+'" })')
        addToFile(string)
        graph.run(query)

def createRelation(S1,S2,graph):
    result = convertHypernymsToString([S1,S2])
    w1 = result[0]
    w2 = result[1]
    #print(w1,w2)

    existsW1 = False 
    existsW2 = False 

    query = '''Match (t:Term) Where t.name = "''' + w1 + '''" Return t'''
    nodes = graph.run(query)

    for node in nodes: 
        existsW1 = True

    query = '''Match (t:Term) Where t.name = "''' + w2 + '''" Return t'''
    nodes = graph.run(query)

    for node in nodes:
        existsW2 = True

    if existsW1 == True and existsW2 == True:
        query = '''MATCH (t1:Term)-[]-(t2:Term) WHERE t1.name = "''' + w1 + '''" and t2.name = "''' + w2 +'''" Return t2'''
        nodes = graph.run(query)
        countNodes = 0
                            
        for node in nodes:
            countNodes += 1
                            
        if countNodes == 0:
            query = '''MATCH (t1:Term),(t2:Term) WHERE t1.name = "''' + w1 + '''" and t2.name = "''' + w2 +'''" 
            MERGE (t1)-[:ISA]->(t2)''' # add property of order 
            graph.run(query)   
            string = '''MATCH (t1:Term),(t2:Term) WHERE t1.name = "''' + w1 + '''" and t2.name = "''' + w2 +'''" 
            \n MERGE (t1)-[:ISA]->(t2)'''
            addToFile(string)         
        return True
    return False  
