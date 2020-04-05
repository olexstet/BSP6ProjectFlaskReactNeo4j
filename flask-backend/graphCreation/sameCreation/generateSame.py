from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import sys,os
ROOT = os.path.abspath(os.path.join(".", os.pardir));
sys.path.append(ROOT)
from graphCreation.graphSetups.commands import *
import random 
from graphCreation.createNodesAndRelations import *
from graphCreation.convertSynsetToString import *

def createSameRelation(dictSame, graph):
    for w in dictSame:
        for s in dictSame[w]: 
            query = ''' Match (t1:Term), (t2:Term) WHERE t1.name = "''' + w +'''" and t2.name = "''' + convertHypernymsToString([s])[0] +'''"
                        Merge (t1)-[:SAME]->(t2)
                        Merge (t2)-[:SAME]->(t1)'''
            graph.run(query)

def findLevelWords(word,level, graph):
    if level > 0:
        query = ''' MATCH (t1:Term)-[:ISA*'''+str(level)+''']-> (t2:Term) WHERE t1.name = "'''+word+'''" RETURN t2'''
        nodes = graph.run(query)

    elif level < 0:
        query = ''' MATCH (t1:Term)<-[:ISA*'''+str(-level)+''']-(t2:Term) WHERE t1.name = "'''+word+'''" RETURN t2'''
        nodes = graph.run(query)
    
    else:
        return [word] 
    
    resultWords = []
    for node in nodes: 
        resultWords.append(node[0]["name"])
    return resultWords 

def takeHypernyms(word, graph):
    query = '''Match (t1:Term)-[:ISA]->(t2:Term) Where t1.name ="'''+word+'''" Return t2 '''
    nodes = graph.run(query)
    result = []
    for node in nodes: 
        result.append(node[0]["name"])
    return result


def generateSame(word,sequence,graph):
    for seq in sequence: 
        level = seq[0]
        numberSame = seq[1]
        wordsHyp = findLevelWords(word, level, graph)
        
        resultHyponyms = {}
        print()
        print("\nSame")
        for w in wordsHyp:
            words = []
            synonyms = wn.synsets(w)
            for s in synonyms: 
                if convertHypernymsToString([s])[0] == w:
                    words.append(s)
            
            for sW in words:
                hypernyms = sW.hypernyms()
                for hyp in hypernyms:
                    hyponyms = hyp.hyponyms()
                    array = convertHypernymsToString(hyponyms)
                    if w in array:
                        index = array.index(w)
                        hyponyms.pop(index)
                    if w not in resultHyponyms:
                        resultHyponyms[w] = hyponyms
                    else:
                        resultHyponyms[w] += hyponyms

        result = {}
        for w in resultHyponyms: 
            array = resultHyponyms[w]
            random.shuffle(array)
            result[w] = array[:numberSame]
            print(w,result[w])

        for w in result: 
            for s in result[w]:
                createNode(s,graph)
        
        createSameRelation(result, graph)
 
#generateSame("apple", [[1,2],[-1,2]], connect())

