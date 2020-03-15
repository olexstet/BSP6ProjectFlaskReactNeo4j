from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random

def connect():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet"))
    return graph 

def fetchDataQ1(word,nRel,nDef):
    graph = connect()
    query = ''' Match (t1:Term)-[:ISA*1..'''+str(nRel)+''']->(t2:Term) Where t1.name ="'''+word+'''" Return t2'''
    nodes = graph.run(query)

    nodesFetched = []
    for node in nodes:
        nameNode = node[0]["name"] 
        if nameNode not in nodesFetched:
            nodesFetched.append(nameNode)
    
    dictWords = []
    for nameNode in nodesFetched: 
        query = ''' Match (t1:Term)<-[:ISA]-(t2:Term) Where t1.name ="'''+nameNode+'''" Return t2'''
        nodes = graph.run(query)
        for node in nodes:
            dictWords.append([node[0]["name"],node[0]["definition"]])
        
    indexArray = []
    for _ in range(nDef):
        index = random.randint(0,len(dictWords)-1)
        defWord = dictWords[index][1]
        while index in indexArray or word in defWord: 
            index = random.randint(0,len(dictWords)-1)
        indexArray.append(index)
    
    finalWords = {}

    for index in indexArray: 
        wordDef = dictWords[index]
        finalWords[wordDef[0]] = wordDef[1]

    print(finalWords)
    return finalWords 


#fetchDataQ1("apple",2,5)