from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random
import requests
import urllib.request
from modules.Q2FetchData import * 

def retrieveSubWords(word, levelDown, numberWords, graph):
    arrayWords = []

    query = ''' Match (t1:Term)<-[:ISA*'''+str(levelDown)+''']-(t2:Term) Where t1.name ="'''+word+'''" Return t2'''
    nodes = graph.run(query)

    for node in nodes:
        arrayWords.append(node[0]['name'])

    random.shuffle(arrayWords)
    arrayWords = arrayWords[:numberWords]
    return arrayWords


def createQuestion3Words(word, levelDown, numberWordsTotal):
    numberSubWords = random.randint(1,numberWordsTotal)
    wordsCategory = retrieveSubWords(word,levelDown,numberSubWords, connect())
    randomWords = chooseRandomWords(fetchAllWords(),numberWordsTotal-len(wordsCategory))
    dictWords = {}
    dictWords[word] = wordsCategory
    dictWords['random'] = randomWords
    return dictWords

#print(createQuestion3Words("apple", 2, 12))