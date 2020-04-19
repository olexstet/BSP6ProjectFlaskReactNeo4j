from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import sys,os
ROOT = os.path.abspath(os.path.join(".", os.pardir));
sys.path.append(ROOT)
from graphCreation.graphSetups.commands import *
from graphCreation.configureSequence import *
from graphCreation.createNodesAndRelations import *
from graphCreation.convertSynsetToString import *
from graphCreation.pathsCreation import *

def removeNonExistedNodes(allPaths, graph):
    results = []
    for array in allPaths: 
        result = []
        for word in array: 
            w = convertHypernymsToString([word])[0]
            query = '''Match (t:Term) Where t.name = "''' + w + '''" Return t'''
            nodes = graph.run(query)
            
            existsW = False 

            for node in nodes: 
                existsW = True

            if existsW: 
                result.append(word)
            
        results.append(result)
    return results 

def checkOtherMeanings(word):
    words = []
    synonyms = wn.synsets(word)
    for s in synonyms: 
        if convertHypernymsToString([s])[0] == word:
            words.append(s)
    return words 

def findHypernyms(word,dist,numberHyp,previousHypernyms,paths):
    result = []
    for synset in previousHypernyms: 
        hypernyms = synset.hypernyms()
        print(synset, hypernyms)
        if type(numberHyp) == int: 
            length = len(hypernyms)
            if length > numberHyp: 
                result += hypernyms[:numberHyp]
                paths[(dist,synset)] = hypernyms[:numberHyp]
            else: 
                result += hypernyms 
                paths[(dist,synset)] = hypernyms
        else:
            result += hypernyms
            paths[(dist,synset)] = hypernyms

    previousHypernyms = result

    previousHypernyms = list(dict.fromkeys(previousHypernyms))
    return previousHypernyms,paths


def generateHypernyms(sequenceHyp, word, graph):
    previousHypernyms = [wn.synsets(word)[0]]
    sequenceHyp = configureSequence(sequenceHyp)
    result = {}
    result[(0,0)] = previousHypernyms
    paths = {}
    dist = 0
    numberHyp = 0
    for seq in sequenceHyp:
        dist = seq[0]
        numberHyp = seq[1]
        previousHypernyms,paths = findHypernyms(word,dist,numberHyp,previousHypernyms,paths)
          
        if (type(dist) and type(numberHyp)) == int:
            result[(seq[0],seq[1])] = previousHypernyms

    createdNodes = []
    for seq in result:
        synsets = result[seq]
        for synset in synsets:
            createNode(synset,graph)
            createdNodes.append(synset)
        
    _,paths = findHypernyms(word,dist+1,numberHyp,previousHypernyms,paths)

    res = formPaths(paths,wn.synsets(word)[0])
    print(res)
    
    res = removeNonExistedNodes(res, graph)
    print("\nRelations hypernyms")
    createdRel = []
    for r in res: 
        for i in range(1,len(r)):
            if [r[i],r[i-1]] not in createdRel:
                createRealation(r[i-1],r[i],graph)
                createdRel.append([r[i],r[i-1]])
                print(r[i-1],r[i])
        
    print("--------------------------------------------------------------")
    return result

#generateHypernyms([[1,5],[5,3]], "apple", connect())