from graphCreation.hypernymsCreation.generateHypernyms import *
from graphCreation.hyponymsCreation.generateHyponyms import *
from graphCreation.sameCreation.generateSame import *
from graphCreation.graphSetups.commands import *

def generateGraph(word,seqHypernyms, seqHyponyms, seqSame):
    graph = connect()
    deleteAll(graph)
    generateHypernyms(seqHypernyms, word, graph)
    generateHyponyms(seqHyponyms, word, graph)
    generateSame(word, seqSame, graph)

#generateGraph("water",[[1,2],[2,2]], [[1,5],[2,3],[3,5]], [[0,30],[1,200],[-2,10]])
