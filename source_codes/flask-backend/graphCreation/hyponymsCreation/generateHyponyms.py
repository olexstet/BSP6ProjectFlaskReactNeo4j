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
from graphCreation.hypernymsCreation.generateHypernyms import removeNonExistedNodes

def checkOtherMeanings(word):
    words = []
    synonyms = wn.synsets(word)
    for s in synonyms: 
        if convertHypernymsToString([s])[0] == word:
            words.append(s)
    return words 

def findHyponyms(word,dist,numberHyp,previousHyponyms,paths):
    result = []

    for synset in previousHyponyms: 
        hyponyms = synset.hyponyms()
        #print(synset, hyponyms)
        if type(numberHyp) == int: 
            length = len(hyponyms)
            if length > numberHyp: 
                result += hyponyms[:numberHyp]
                paths[(dist,synset)] = hyponyms[:numberHyp]
            else: 
                result += hyponyms 
                paths[(dist,synset)] = hyponyms
        else:
            result += hyponyms
            paths[(dist,synset)] = hyponyms

    previousHyponyms = result

    previousHyponyms = list(dict.fromkeys(previousHyponyms))
    return previousHyponyms,paths


def generateHyponyms(sequenceHyp, word, graph):
    previousHyponyms = [wn.synsets(word)[0]]
    sequenceHyp = configureSequence(sequenceHyp)
    result = {}
    result[(0,0)] = previousHyponyms
    paths = {}
    dist = 0
    numberHyp = 0
    for seq in sequenceHyp:
        dist = seq[0]
        numberHyp = seq[1]
        previousHyponyms,paths = findHyponyms(word,dist,numberHyp,previousHyponyms,paths)
          
        if (type(dist) and type(numberHyp)) == int:
            result[(seq[0],seq[1])] = previousHyponyms

    # print all hyponyms finded in the sequence
    """
    print("Hyponyms in sequence:")
    for pos in result: 
        print(pos, result[pos])
    """

    createdNodes = []
    for seq in result:
        synsets = result[seq]
        for synset in synsets:
            createNode(synset,graph)
            createdNodes.append(synset)
        
    _,paths = findHyponyms(word,dist+1,numberHyp,previousHyponyms,paths)

    """
    print("Paths of hyponyms:")
    for p in paths: 
        print(p,paths[p])
    """

    res = formPaths(paths,wn.synsets(word)[0])

    """
    print("All possible paths:")
    for r in res:
        print(r)
    """

    #print("\nRelations hyponyms")
    res = removeNonExistedNodes(res, graph)
    createdRel = []
    for r in res: 
        for i in range(1,len(r)):
            if [r[i],r[i-1]] not in createdRel:
                createRelation(r[i],r[i-1],graph)
                createdRel.append([r[i],r[i-1]])
                #print(r[i-1],r[i])

    return result

