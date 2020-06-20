from graphCreation.hypernymsCreation.generateHypernyms import *
from graphCreation.hyponymsCreation.generateHyponyms import *
from graphCreation.sameCreation.generateSame import *
from graphCreation.graphSetups.commands import *
from nltk.corpus import wordnet as wn

def check_term_existance(term): # check for the web app if the entered term exists in wordNet library 
    english_vocabulary = set(w.lower() for w in nltk.corpus.words.words()) # fetch all possible words in wordNet 
    if term in english_vocabulary: # check existance 
        return True
    else: 
        return False 

# function for generating the graph which accepts a term, sequence of hypernyms (level, #hypernyms), sequence of hyponyms, sequence of Same
def generateGraph(word,seqHypernyms, seqHyponyms, seqSame):
    graph = connect() # connection to graph 
    deleteAll(graph) # delete existent graph 
    generateHypernyms(seqHypernyms, word, graph) # step 1: create hypernyms 
    generateHyponyms(seqHyponyms, word, graph)  # step 2: create hyponyms 
    generateSame(word, seqSame, graph) # step 3: create same terms and relations 

#generateGraph("water",[[1,2],[2,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,200],[-2,10]])
