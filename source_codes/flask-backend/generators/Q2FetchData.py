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

def typeWord(word, graph):
    query = '''Match (t:Term) Where t.name = "'''+word+'''" Return t'''
    nodes = graph.run(query)
    nodeW = []

    for node in nodes:
        nodeW = node 
        break 

    return nodeW[0]['type']

def fetchAllWords():
    wordlist = wordsCorpus.words()
    return wordlist 

def exactWordComparaison(initW, synsetsW):
    for s in synsetsW:
        nameS = s.name().split(".")[0]
        if initW == nameS: 
            return [s]
    return []


def chooseRandomWords(words,N, typeW):
    retrievedWords = []
    defType = {"Name": "n", "Verbe": "v", "Adjective": "a", "Adverbe": "r"}

    for i in range(N):
        index = random.randint(0, len(words)-1)
        while len(wn.synsets(words[index])) == 0:
            index = random.randint(0, len(words)-1)
        typeWR = wn.synsets(words[index])[0].pos()
        while typeWR != defType[typeW]:
            index = random.randint(0, len(words)-1)
            while len(wn.synsets(words[index])) == 0:
                index = random.randint(0, len(words)-1)
            syn = exactWordComparaison(words[index], wn.synsets(words[index]))
            if len(syn) > 0:
                typeWR = syn[0].pos()
        print(words[index],wn.synsets(words[index]))
        retrievedWords.append(words[index])

    random.shuffle(retrievedWords)
    return retrievedWords 

def retrieveWordsCategory(word, levelUp, levelDown, numberWords, graph):
    query = ''' Match (t1:Term)-[:ISA*'''+str(levelUp)+''']->(t2:Term) Where t1.name ="'''+word+'''" Return t2'''
    nodes = graph.run(query)

    index = 0
    arrayNames = []
    for node in nodes:
        arrayNames.append(node[0]['name'])
    
    index = random.randint(0,len(arrayNames)-1)
    category = arrayNames[index]

    arrayWords = []

    query = ''' Match (t1:Term)<-[:ISA*'''+str(levelDown)+''']-(t2:Term) Where t1.name ="'''+category+'''" Return t2'''
    nodes = graph.run(query)

    for node in nodes:
        arrayWords.append(node[0]['name'])

    words = []
    for w in arrayWords: 
        query = ''' Match (t1:Term)-[:SAME]->(t2:Term) Where t1.name ="'''+ w +'''" Return t2'''
        nodes = graph.run(query)
        for node in nodes: 
            words.append(node[0]['name'])

    words = list(set(words))
    random.shuffle(words)
    words = words[:numberWords]
    return category, words


def createQuestion2Words(word, levelUp,levelDown, numberWordsCategory, numberWordsTotal):
    typeW = typeWord(word, connect())
    category,wordsCategory = retrieveWordsCategory(word, levelUp,levelDown, numberWordsCategory, connect())
    randomWords = chooseRandomWords(fetchAllWords(),numberWordsTotal-numberWordsCategory, typeW)
    dictWords = {}
    dictWords[category] = wordsCategory
    dictWords['random'] = randomWords
    return dictWords

#print(createQuestion2Words("apple", 2,2, 5, 12))