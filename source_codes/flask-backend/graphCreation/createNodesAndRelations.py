from graphCreation.convertSynsetToString import *
from nltk.corpus import wordnet as wn

# create a custom property for node (label)
def generateLabel(labelSequence, separation): # string sequence , separation = ":",",", "anything"
    result = ""
    for i in range(len(labelSequence)):
        element = labelSequence[i]
        if i != len(labelSequence)-1:
            result += element + separation
        else:
            result += element 
    return result

# Create a node for a term
def createNode(S,graph): # synset, graph 
    result = convertHypernymsToString([S]) # convert from synset to string (name of the synset)
    defType = {"n": "Name", "v": "Verbe", "a": "Adjective", "r": "Adverbe"} # possible types of words 

    w = result[0] # fetch term 

    typeW = S.pos() # fetch type of synset 
    typeW = defType[typeW] # translate type into prefered type 

    label = generateLabel([w,typeW], "::")

    definition = wn.synsets(w)[0].definition()
    definition = definition.replace('"','')

    query = "Match (t:Term) return t" # neo4j query for fetching all nodes 

    countNodes = 0
    nodes = graph.run(query)
    names =[]
    for node in nodes:
        names.append(node[0]['name'])
    #print(names)

    if w in names:
        countNodes += 1
        
    if countNodes == 0: # if no similar nodes exist, create new node 
        query = 'MERGE (t:Term {name: '+'"'+w+'", definition: "'+ definition + '" , type: "'+typeW+'" , label: "'+label+'" })'
        graph.run(query)

#create relations between two synsets 
def createRelation(S1,S2,graph):
    result = convertHypernymsToString([S1,S2])
    w1 = result[0] # fetch term name 
    w2 = result[1]
    #print(w1,w2)

    existsW1 = False 
    existsW2 = False 

    query = '''Match (t:Term) Where t.name = "''' + w1 + '''" Return t''' # find first term 
    nodes = graph.run(query)

    for node in nodes: 
        existsW1 = True

    query = '''Match (t:Term) Where t.name = "''' + w2 + '''" Return t''' # find second term 
    nodes = graph.run(query)

    for node in nodes:
        existsW2 = True

    if existsW1 == True and existsW2 == True: # if both exist 
        query = '''MATCH (t1:Term)-[]-(t2:Term) WHERE t1.name = "''' + w1 + '''" and t2.name = "''' + w2 +'''" Return t2''' # look if a relation exists already a 
        nodes = graph.run(query)
        countNodes = 0
                            
        for node in nodes:
            countNodes += 1
                            
        if countNodes == 0: # if no relations, create one 
            query = '''MATCH (t1:Term),(t2:Term) WHERE t1.name = "''' + w1 + '''" and t2.name = "''' + w2 +'''" 
            MERGE (t1)-[:ISA]->(t2)'''  
            graph.run(query)   
                   
        return True
    return False  
