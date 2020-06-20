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

def checkOtherMeanings(word): # check other possible meanings for a term in synset(future development if needed)
    words = []
    synonyms = wn.synsets(word)
    for s in synonyms: 
        if convertHypernymsToString([s])[0] == word:
            words.append(s)
    return words 

def findHyponyms(word,dist,numberHyp,previousHyponyms,paths):  # find next hyponyms 
    result = []

    for synset in previousHyponyms: # go though already founded hyponyms 
        hyponyms = synset.hyponyms() # fetch new hyponyms 
        if type(numberHyp) == int: 
            length = len(hyponyms)
            if length > numberHyp: # if number of hyponyms smaller than number founded hyponyms 
                result += hyponyms[:numberHyp] # add to already founded hyponyms for the leve
                paths[(dist,synset)] = hyponyms[:numberHyp] # add to path 
            else: # if exactly the same number or lower 
                result += hyponyms  # add to already founded hyponyms for the level 
                paths[(dist,synset)] = hyponyms
        else: # if all hypernyms needed 
            result += hyponyms 
            paths[(dist,synset)] = hyponyms

    previousHyponyms = result

    previousHyponyms = list(dict.fromkeys(previousHyponyms))
    return previousHyponyms,paths


def generateHyponyms(sequenceHyp, word, graph): # create hyponyms 
    previousHyponyms = [wn.synsets(word)[0]] # initial hyponym = initial term 
    sequenceHyp = configureSequence(sequenceHyp)
    result = {}
    result[(0,0)] = previousHyponyms
    paths = {}
    dist = 0
    numberHyp = 0
    for seq in sequenceHyp:
        dist = seq[0] # level 
        numberHyp = seq[1] # number hyponyms needed for level 
        previousHyponyms,paths = findHyponyms(word,dist,numberHyp,previousHyponyms,paths) # find next hyponyms 
          
        if (type(dist) and type(numberHyp)) == int:
            result[(seq[0],seq[1])] = previousHyponyms # used for storing the only hyponyms needed to create 

    createdNodes = []
    # create hyponyms nodes 
    for seq in result:
        synsets = result[seq]
        for synset in synsets:
            createNode(synset,graph) # create node function 
            createdNodes.append(synset)
        
    _,paths = findHyponyms(word,dist+1,numberHyp,previousHyponyms,paths)


    res = formPaths(paths,wn.synsets(word)[0]) # find all possible paths  

    res = removeNonExistedNodes(res, graph) # remove terms which don't exist in graph 
    # Create Relations 
    createdRel = []
    for r in res: 
        for i in range(1,len(r)):
            if [r[i],r[i-1]] not in createdRel:
                createRelation(r[i],r[i-1],graph)
                createdRel.append([r[i],r[i-1]])
             

    return result

