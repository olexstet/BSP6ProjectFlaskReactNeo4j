from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random
import requests
import urllib.request
from nltk.corpus import words as wordsCorpus


def connect():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet"))
    return graph 

def typeWord(word, graph): # fetch type of term 
    query = '''Match (t:Term) Where t.name = "'''+word+'''" Return t'''
    nodes = graph.run(query)
    nodeW = []

    for node in nodes:
        nodeW = node 
        break 

    return nodeW[0]['type']

def fetchAllWords(): # fetch the words from wordNet corpus 
    wordlist = wordsCorpus.words()
    return wordlist 

def exactWordComparaison(initW, synsetsW): # synset word has to be the same as another word 
    for s in synsetsW:
        nameS = s.name().split(".")[0]
        if initW == nameS: 
            return [s]
    return []


def chooseRandomWords(words,N, typeW): # choose randomly missed words from wordNet corpus 
    retrievedWords = []
    defType = {"Name": "n", "Verbe": "v", "Adjective": "a", "Adverbe": "r"}

    for i in range(N):
        index = random.randint(0, len(words)-1)
        while len(wn.synsets(words[index])) == 0: # words has to exists in corpus 
            index = random.randint(0, len(words)-1)
        typeWR = wn.synsets(words[index])[0].pos() # take the type of word 
        while typeWR != defType[typeW]: # type has to be the same 
            index = random.randint(0, len(words)-1)
            while len(wn.synsets(words[index])) == 0: 
                index = random.randint(0, len(words)-1)
            syn = exactWordComparaison(words[index], wn.synsets(words[index])) # fetch the right word 
            if len(syn) > 0:
                typeWR = syn[0].pos()
        print(words[index],wn.synsets(words[index]))
        retrievedWords.append(words[index])

    random.shuffle(retrievedWords)
    return retrievedWords 

def retrieveWordsCategory(word, levelUp, levelDown, numberWords, graph):
    query = ''' Match (t1:Term)-[:ISA*'''+str(levelUp)+''']->(t2:Term) Where t1.name ="'''+word+'''" Return t2''' # go n level up in ISA relations from initial term 
    nodes = graph.run(query)

    index = 0
    arrayNames = []
    for node in nodes:
        arrayNames.append(node[0]['name']) # fetch the names of nodes 
    
    index = random.randint(0,len(arrayNames)-1)
    category = arrayNames[index] # choose randomly one category 

    words = []

    query = """Match (t1:Term)-[:ISA*1.."""+str(levelDown)+"""]->(t2:Term {name: '"""+ category + """'}) return t1""" # look on hyponyms created in graph 
    nodes = graph.run(query)

    for node in nodes:
        if node[0]['name'] != word:
            words.append(node[0]['name']) # take names of nodes 

    words = list(set(words)) # remove duplicates in case 
    random.shuffle(words) # shuffle all the obtained words for randomless 
    words = words[:numberWords] # take n words 
    return category, words


def createQuestion2Words(word, levelUp,levelDown, numberWordsTotal): # second generator
    typeW = typeWord(word, connect())
    numberWordsCategory = random.randint(1,numberWordsTotal) # number of words for a category 
    category,wordsCategory = retrieveWordsCategory(word, levelUp,levelDown, numberWordsCategory, connect()) # correct words 
    randomWords = chooseRandomWords(fetchAllWords(),numberWordsTotal-numberWordsCategory, typeW) # random words 
    dictWords = {}
    dictWords[category] = wordsCategory # put in dictionary correct words 
    dictWords['random'] = randomWords # wrong words in dictionary 
    return dictWords

#print(createQuestion2Words("apple", 2,2, 5, 12))
