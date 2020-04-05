from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random
import requests
import urllib.request


def connect():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet"))
    return graph 

def fetchAllWords():
    word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    words = long_txt.splitlines()

    return words 

def chooseRandomWords(words,N):
    retrievedWords = []
    for i in range(N):
        index = random.randint(0, len(words)-1)
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

    random.shuffle(words)
    words = words[:numberWords]
    return category, words


def createQuestion2Words(word, levelUp,levelDown, numberWordsCategory, numberWordsTotal):
    print("start")
    category,wordsCategory = retrieveWordsCategory(word, levelUp,levelDown, numberWordsCategory, connect())
    randomWords = chooseRandomWords(fetchAllWords(),numberWordsTotal-numberWordsCategory)
    dictWords = {}
    dictWords[category] = wordsCategory
    dictWords['random'] = randomWords
    return dictWords

#print(createQuestion2Words("apple", 2,2, 5, 12))