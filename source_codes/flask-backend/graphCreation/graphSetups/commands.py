from py2neo import Graph,Node,Relationship

def connect():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet"))
    return graph 

def deleteAll(graph):
    graph.delete_all() # clear graph 
