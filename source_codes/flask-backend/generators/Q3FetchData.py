from py2neo import Graph,Node,Relationship
import nltk 
from nltk.corpus import wordnet as wn
import random
import requests
import urllib.request
from generators.Q2FetchData import * 

def retrieveSubWords(word, levelDown, numberWords, graph): # retieve hyponyms at a level 
    arrayWords = []

    query = ''' Match (t1:Term)<-[:ISA*1..'''+str(levelDown)+''']-(t2:Term) Where t1.name ="'''+word+'''" Return t2''' # fetch hyponyms for a level 
    nodes = graph.run(query)

    for node in nodes:
        arrayWords.append(node[0]['name'])

    random.shuffle(arrayWords)
    arrayWords = arrayWords[:numberWords] # take n words of hyponyms 
    return arrayWords


def createQuestion3Words(word, levelDown, numberWordsTotal):
    typeW = typeWord(word, connect())
    numberSubWords = random.randint(1,numberWordsTotal)
    wordsCategory = retrieveSubWords(word,levelDown,numberSubWords, connect()) # correct words 
    randomWords = chooseRandomWords(fetchAllWords(),numberWordsTotal-len(wordsCategory), typeW) # random words 
    dictWords = {}
    dictWords[word] = wordsCategory
    dictWords['random'] = randomWords
    return dictWords

#print(createQuestion3Words("apple", 2, 12))
