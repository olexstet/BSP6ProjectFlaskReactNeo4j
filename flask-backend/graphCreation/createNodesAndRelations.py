from graphCreation.convertSynsetToString import *
from nltk.corpus import wordnet as wn

def createNode(S,graph):
    result = convertHypernymsToString([S])
    w = result[0]
    definition = wn.synsets(w)[0].definition()
    definition = definition.replace('"','')
    query = 'MERGE (t:Term {name: '+'"'+w+'", definition: "'+ definition + '" })'
    graph.run(query)

def createRealation(S1,S2,graph):
    result = convertHypernymsToString([S1,S2])
    w1 = result[0]
    w2 = result[1]

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
        return True
    return False  
