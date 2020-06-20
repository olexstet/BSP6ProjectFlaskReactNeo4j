from py2neo import Graph,Node,Relationship

def connect(): # connect and fetch the graph 
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "olexstet")) # use url, auth = {username, password}
    return graph 

def deleteAll(graph):
    graph.delete_all() # delete graph 
