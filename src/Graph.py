class Node:
    id, name, indegree, outdegree = None, None, None, None   
   
    
    def __init__(self, id, name):     
        self.id = id
        self.name = name
        self.indegree = 0
        self.outdegree = 0        
                
    def increase_indegree(self):
        self.indegree = self.indegree + 1        

    def increase_outdegree(self):
        self.outdegree = self.outdegree + 1


class Edge:
    id, source, dest, weight = None, None, None, None

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.id = GraphSupport.edgeIdGenerator(source, dest)
        self.weight = 1
        #calcula grau no momento da criacao do edge
        source.increase_outdegree()
        dest.increase_indegree()
        

    def increase_weight(self):
        self.weight =  self.weight + 1
        

class Graph:
    nodes, edges = None, None
   
    
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    

class GraphSupport:

    @staticmethod
    def edgeIdGenerator(source, dest):
        id = source.id + "_" + dest.id
        return id
                
    #metodo auxiliar para colocar os nodes em um dict
    @staticmethod
    def loadNode(nodes, id, name):
        
        if(nodes.get(id) is None):
            node = Node(id, name)
            nodes[id] = node        
        return nodes

    # metodo auxiliar para colocar os edges em um dict
    @staticmethod
    def loadEdge(edges, source, dest):
        if(source.id != dest.id):   
            id = GraphSupport.edgeIdGenerator(source, dest)
            if(edges.get(id) is None):
                edge = Edge(source, dest)
                edges[id] = edge                    
            else:
                edges.get(id).increase_weight()
        return edges

        
