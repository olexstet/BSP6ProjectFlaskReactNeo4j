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

def createSameRelation(dictSame, graph): # same relations creation, inputs: dictSame key is a term, value is also the term, both are related 
    for w in dictSame:
        for s in dictSame[w]: 
            query = ''' Match (t1:Term), (t2:Term) WHERE t1.name = "''' + w +'''" and t2.name = "''' + convertHypernymsToString([s])[0] +'''"
                        Merge (t1)-[:SAME]->(t2)
                        Merge (t2)-[:SAME]->(t1)'''
            
            graph.run(query)

def createISARelation(wordsSame, hypernyms, graph): # Create ISA relations for SAME terms 
    for w in wordsSame:
        isaWords = hypernyms[w]
        for sameWord in wordsSame[w]:
            for isaWord in isaWords:
                hypernymsWord = sameWord.hypernyms()
                if isaWord in hypernymsWord: 
                    query = ''' MATCH (t1:Term {name:"''' + convertHypernymsToString([sameWord])[0] + '''"}), (t2:Term {name:"'''+ convertHypernymsToString([isaWord])[0]+'''"}) 
                            MERGE (t1)-[:ISA]->(t2)'''
                    graph.run(query)

def findLevelWords(word,level, graph):# fetch all the terms at a certain level 
    if level > 0: # positive level 
        query = ''' MATCH (t1:Term)-[:ISA*'''+str(level)+''']-> (t2:Term) WHERE t1.name = "'''+word+'''" RETURN t2'''
        nodes = graph.run(query)

    elif level < 0: # negative level (below inital term)
        query = ''' MATCH (t1:Term)<-[:ISA*'''+str(-level)+''']-(t2:Term) WHERE t1.name = "'''+word+'''" RETURN t2'''
        nodes = graph.run(query)
    
    else:
        return [word] # if level 0 return inital term 
    
    resultWords = []
    for node in nodes: 
        resultWords.append(node[0]["name"]) # fetch all terms at a level 
    return resultWords 


def generateSame(word,sequence,graph): # create SAME nodes and relations 
    for seq in sequence: 
        level = seq[0]
        numberSame = seq[1] # number of same nodes per level 
        wordsLevel= findLevelWords(word, level, graph) # fetch all the terms at a level 

        resultHyponyms = {}

        allHypernyms = {}
        for w in wordsLevel: 
            words = []
            synonyms = wn.synsets(w)
            for s in synonyms: 
                if convertHypernymsToString([s])[0] == w:
                    words.append(s)
                    break # do not take other synonyms what are close to the original meaning 
            
            for sW in words:
                hypernyms = sW.hypernyms() # find the hypernyms for a term 
                allHypernyms[sW] = hypernyms 
                for hyp in hypernyms:
                    hyponyms = hyp.hyponyms() # find hyponyms for a hypernym 
                    array = convertHypernymsToString(hyponyms)
                    if w in array: # remove term fro which the hypernyms are selected if exists 
                        index = array.index(w)
                        hyponyms.pop(index)
                    if w not in resultHyponyms:
                        resultHyponyms[w] = hyponyms # add to the result of Same terms array 
                    else:
                        resultHyponyms[w] += hyponyms

        result = {}
        for w in resultHyponyms: 
            array = resultHyponyms[w]
            random.shuffle(array) # shuffle the array of terms 
            result[w] = array[:numberSame] # selected only the number of needed SAME terms 
           
        for w in result: # create nodes for SAME terms
            for s in result[w]:
                createNode(s,graph)

        hyper = {}
        for w in allHypernyms:
            w2 = convertHypernymsToString([w])
            hyper[w2[0]] = allHypernyms[w]
       
        #Create relations 
        createISARelation(result, hyper, graph)
        createSameRelation(result, graph)
 
#generateSame("apple", [[1,2],[-1,2]], connect())

