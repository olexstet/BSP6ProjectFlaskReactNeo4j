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

def removeNonExistedNodes(allPaths, graph): # remove nodes which are not present in the graph 
    results = []
    for array in allPaths: 
        result = []
        for word in array: 
            w = convertHypernymsToString([word])[0] # fetch name of synset 
            query = '''Match (t:Term) Where t.name = "''' + w + '''" Return t''' # check if term exists in graph 
            nodes = graph.run(query)
            
            existsW = False 

            for node in nodes: # if node exists, set to true 
                existsW = True

            if existsW: 
                result.append(word) # if exists add to array for saving the node 
            
        results.append(result)
    return results # return array of array of nodes present in the graph, also can be see as all paths of existent nodes 

def checkOtherMeanings(word): # not used, but can be used for future development (check if the term has several meaning in wordNet )
    words = []
    synonyms = wn.synsets(word)
    for s in synonyms: 
        if convertHypernymsToString([s])[0] == word:
            words.append(s)
    return words 

def findHypernyms(word,dist,numberHyp,previousHypernyms,paths):
    result = []
    for synset in previousHypernyms: # look on previous hypernyms founded 
        hypernyms = synset.hypernyms() # find all hypernyms based on synset 
        #print(synset, hypernyms)
        if type(numberHyp) == int: # if the number of hypernyms needed is not 'All' and is integer 
            length = len(hypernyms)
            if length > numberHyp: # fetch only the number of needed hypernyms, if it exists more than we need 
                result += hypernyms[:numberHyp] # add to new founded hypernyms 
                paths[(dist,synset)] = hypernyms[:numberHyp] # add to the path 
            else: # if exactly the number of hypernyms needed or lower, take all possible hypernyms for synset 
                result += hypernyms 
                paths[(dist,synset)] = hypernyms
        else: # if 'All' hypernyms needed 
            result += hypernyms 
            paths[(dist,synset)] = hypernyms

    previousHypernyms = result # store all new founded hypernyms 

    previousHypernyms = list(dict.fromkeys(previousHypernyms))
    return previousHypernyms,paths


def generateHypernyms(sequenceHyp, word, graph): # allow to create hypernyms in the graph for a term 
    previousHypernyms = [wn.synsets(word)[0]] # fecth initial term 
    sequenceHyp = configureSequence(sequenceHyp) # fill the gaps 
    result = {}
    result[(0,0)] = previousHypernyms
    paths = {}
    dist = 0
    numberHyp = 0
    for seq in sequenceHyp:# go though the sequence of needed hypernyms (level, number hypernyms)
        dist = seq[0] # level 
        numberHyp = seq[1] # number needed 
        previousHypernyms,paths = findHypernyms(word,dist,numberHyp,previousHypernyms,paths) # find for a level the hypernyms 
          
        if (type(dist) and type(numberHyp)) == int:
            result[(seq[0],seq[1])] = previousHypernyms # founded hypernyms are previous hypernyms for next iteration 

    # Create nodes
    createdNodes = []
    for seq in result:
        synsets = result[seq]
        for synset in synsets:
            createNode(synset,graph)
            createdNodes.append(synset)
        
    _,paths = findHypernyms(word,dist+1,numberHyp,previousHypernyms,paths) # add next level hypernyms 

    res = formPaths(paths,wn.synsets(word)[0]) # all the possible paths from inital term to all hypernyms 
    
    res = removeNonExistedNodes(res, graph) # remove nodes which don't exist in the graph 
    
    # Create Relations 
    createdRel = []
    for r in res: 
        for i in range(1,len(r)):
            if [r[i],r[i-1]] not in createdRel:
                createRelation(r[i-1],r[i],graph)
                createdRel.append([r[i],r[i-1]])
        
    return result

#generateHypernyms([[1,5],[5,3]], "apple", connect())
