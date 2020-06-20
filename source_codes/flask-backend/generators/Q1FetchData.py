from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random

def connect(): # connect to neo4j graph database 
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet"))
    return graph 

def fetchDataQ1(word,nRel,nDef): # first generator for defintions 
    graph = connect()
    query = ''' Match (t1:Term)-[:ISA*0..'''+str(nRel)+''']->(t2:Term) Where t1.name ="'''+word+'''" Return t2''' # fetch all ISA nodes 
    nodes = graph.run(query) # run query 
    nodesFetched = []
    for node in nodes:
        nameNode = node[0]["name"] 
        if nameNode not in nodesFetched:
            nodesFetched.append(nameNode) # saved all fetched nodes 
    
    dictWords = []
    for nameNode in nodesFetched: 
        query = ''' Match (t1:Term)-[:SAME]->(t2:Term) Where t1.name ="'''+nameNode+'''" Return t2''' # for each fetched node look at nodes relating with same relations 
        nodes = graph.run(query) 
        for node in nodes:
            dictWords.append([node[0]["name"],node[0]["definition"]]) #take the defintion of 'SAME' nodes 

    indexArray = []
    # choose the positions of definitions to take 
    for _ in range(nDef-1):
        index = random.randint(0,len(dictWords)-1)
        defWord = dictWords[index][1]
        while index in indexArray or word in defWord: # do not take two time the defintion 
            defWord = dictWords[index][1]
            index = random.randint(0,len(dictWords)-1)
        indexArray.append(index)
    
    finalWords = {}
    query = ''' Match (t1:Term) Where t1.name ="'''+word+'''" Return t1'''
    nodes = graph.run(query)
    for node in nodes: 
        finalWords[word] = node[0]["definition"] # take the defintion of initial term 
        
    for index in indexArray: 
        wordDef = dictWords[index]
        finalWords[wordDef[0]] = wordDef[1] # take all other definitions 

    return finalWords 


#fetchDataQ1("apple",2,5)
