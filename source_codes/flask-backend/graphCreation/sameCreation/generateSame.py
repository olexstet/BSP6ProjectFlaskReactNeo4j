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

def addToFile(string):
    f = open("graphCreation/cypherScript.txt", "r")
    saveD = f.read()
    f.close()
    f = open("graphCreation/cypherScript.txt", "w")
    f.write(saveD)
    f.write(string+"\n")
    f.close()

def createSameRelation(dictSame, graph):
    for w in dictSame:
        for s in dictSame[w]: 
            query = ''' Match (t1:Term), (t2:Term) WHERE t1.name = "''' + w +'''" and t2.name = "''' + convertHypernymsToString([s])[0] +'''"
                        Merge (t1)-[:SAME]->(t2)
                        Merge (t2)-[:SAME]->(t1)'''
            #addToFile(str(query))
            graph.run(query)

def createISARelation(wordsSame, hypernyms, graph):
    for w in wordsSame:
        isaWords = hypernyms[w]
        for sameWord in wordsSame[w]:
            for isaWord in isaWords:
                hypernymsWord = sameWord.hypernyms()
                if isaWord in hypernymsWord:
                    query = ''' MATCH (t1:Term {name:"''' + convertHypernymsToString([sameWord])[0] + '''"}), (t2:Term {name:"'''+ convertHypernymsToString([isaWord])[0]+'''"}) 
                            MERGE (t1)-[:ISA]->(t2)'''
                    graph.run(query)
                    print(convertHypernymsToString([sameWord])[0] , convertHypernymsToString([isaWord])[0])

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


def generateSame(word,sequence,graph):
    for seq in sequence: 
        level = seq[0]
        numberSame = seq[1]
        wordsLevel= findLevelWords(word, level, graph)

        resultHyponyms = {}
        #print()
        #print("\nSame")

        allHypernyms = {}
        for w in wordsLevel:
            words = []
            synonyms = wn.synsets(w)
            for s in synonyms: 
                if convertHypernymsToString([s])[0] == w:
                    words.append(s)
                    break # do not take othersynonyms what are close to the original meaning 
            
            for sW in words:
                hypernyms = sW.hypernyms()
                allHypernyms[sW] = hypernyms
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
            #print(w,result[w])

        for w in result: 
            for s in result[w]:
                createNode(s,graph)

        hyper = {}
        for w in allHypernyms:
            w2 = convertHypernymsToString([w])
            hyper[w2[0]] = allHypernyms[w]
        print(result, hyper)
        createISARelation(result, hyper, graph)
        createSameRelation(result, graph)
 
#generateSame("apple", [[1,2],[-1,2]], connect())

