import sys
import json
import codecs
import os


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
        self.id = edgeIdGenerator(source, dest)
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
        

class Work:
	id = None 
	authorList = None
	paperName = None
	edicao = None
	downloadUrl = None

	def __init__(self, id, authorList, paperName, edicao, downloadUrl):
		self.id = id
		self.authorList = []
		self.paperName = paperName
		self.edicao = edicao
		self.downloadUrl = downloadUrl
		if authorList:
			for author in authorList:
				if author:
					a = author.strip()
					a = a.upper()
					a = ' '.join([word for word in a.split() if word not in ['DE', 'DES', 'DA', 'DAS', 'DO', 'DOS']])
					nameVariantArray = a.split()
					nameVariant = ''
					for idx, name in enumerate(nameVariantArray):
						if 0 == idx:
							nameVariant = nameVariantArray[0]
						else:
							nameVariant = nameVariant + ' ' + name[0] + '.'
							nameVariant = nameVariant.strip()
					self.authorList.append(nameVariant)

def absFilePath(fileName, folder):    
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder,fileName)
    return os.path.abspath(path)

def countWorkAloneByEdicao(workList):
	edicaoDict = {}
	for work in workList:
		if edicaoDict.get(work.edicao) is None:
			edicaoDict[work.edicao] = 0
		if (work.authorList) and (len(work.authorList) == 1):
			edicaoDict[work.edicao] = edicaoDict[work.edicao] + 1
			print work.id
		#if (not work.authorList):
			#print work.paperName, work.edicao

	folder = 'data' + os.sep + 'report'
	fileParam = absFilePath('countWorkAloneByEdicao' , folder)
	with codecs.open(fileParam, 'w', encoding='utf-8') as f:
		f.write('edicao;Numero Trabalhos Sem Colaboracao \n')
		for edicao in edicaoDict:
			f.write(str(edicao) + ';' + str(edicaoDict[edicao]) + '\n')

def countWorkByEdicao(workList):
    edicaoDict = {}
    for work in workList:
    	if edicaoDict.get(work.edicao) is None:
    		edicaoDict[work.edicao] = 0
    	edicaoDict[work.edicao] = edicaoDict[work.edicao] + 1

    folder = 'data' + os.sep + 'report'
    fileParam = absFilePath('workCountByEdicao' , folder)
    with codecs.open(fileParam, 'w', encoding='utf-8') as f:
    	f.write('edicao;Numero de Trabalhos \n')
    	for edicao in edicaoDict:
			f.write(str(edicao) + ';' + str(edicaoDict[edicao]) + '\n')


def countAuthors(workList):
    authorDict = {}   
    for work in workList:
        for author in work.authorList:
        	if author:
        		if authorDict.get(author) is None:
        		    authorDict[author] = 0
                authorDict[author] = authorDict[author] + 1
                

    folder = 'data' + os.sep + 'report'
    fileParam = absFilePath('orderedAuthors' , folder)
    
    with codecs.open(fileParam, 'w', encoding='utf-8') as f:
        for author in sorted(authorDict):
    	    f.write(author + ' ; ' + str(authorDict[author]) + ' \n')
 	return authorDict

def countAuthorsByEdicao(workList):
	edicaoDict = {}
	for work in workList:
		if edicaoDict.get(work.edicao) is None:
			edicaoDict[work.edicao] = []
		edicaoDict[work.edicao].append(work)
    
	folder = 'data' + os.sep + 'report'
	fileParam = absFilePath('authorsCountByEdicao' , folder)
	text = ''
	for edicao in sorted(edicaoDict):
	    authorDict = {}   
	    workList = edicaoDict[edicao]
	    for work in workList:
		    for author in work.authorList:
			    if authorDict.get(author) is None:
				    authorDict[author] = 0
			    authorDict[author] = authorDict[author] + 1
	    text = text + str(edicao) + ';' + str(len(authorDict)) + ';' + str((1.0 * len(authorDict))/len(workList)) + '\n'			    

    
	with codecs.open(fileParam, 'w', encoding='utf-8') as f:
	    f.write('edicao ; Numero de Autores; Media de Autores \n' )
	    f.write(text)    


def edgeIdGenerator(source, dest):
    id = source.id + "_" + dest.id
    return id
                
#metodo auxiliar para colocar os nodes em um dict
def loadNode(nodes, id, name):
	
	if(nodes.get(id) is None):
		node = Node(id, name)
		nodes[id] = node        
	return nodes

# metodo auxiliar para colocar os edges em um dict
def loadEdge(edges, source, dest):
    if(source.id != dest.id):   
        id = edgeIdGenerator(source, dest)
        if(edges.get(id) is None):
            edge = Edge(source, dest)
            edges[id] = edge                    
        else:
            edges.get(id).increase_weight()
    return edges


def buildGraph(workList):
	nodeDict = {}
	edgeDict = {}
	for work in workList:
		for author in work.authorList:
			if author:
				nodeDict =  loadNode(nodeDict, author, author)
	
	for work in workList:
		for author in work.authorList:
			for author2 in work.authorList:
				if author and author2:
					source = nodeDict.get(author)
					dest = nodeDict.get(author2)

					#print str(source) + ' ; ' + source.id
					loadEdge(edgeDict, source, dest)
					loadEdge(edgeDict, dest, source)
	graph = Graph(nodeDict, edgeDict)
	return graph

def printGml(graph, fileName = 'authorsColaborationGML.gml'):   
	
    nodes = graph.nodes
    edges = graph.edges
    folder = 'data' + os.sep + 'report'
    authorGML = absFilePath(fileName, folder)
    with codecs.open(authorGML, 'w', 'utf-8') as gml:
        gml.write("graph \n")
        gml.write("[ \n")
        gml.write("    directed 0 \n")
        for key in nodes:
            gml.write("    node \n")
            gml.write("    [ \n")
            gml.write('      id "' + key + '" \n')
            gml.write('      label "' + key + '"')
            gml.write("    ] \n")
        for key in edges:
            gml.write("    edge \n")
            gml.write("    [ \n")
            gml.write('      source "' + edges.get(key).source.id + '" \n')
            gml.write('      target "' + edges.get(key).dest.id + '" \n')
            gml.write('      weight ' + str(edges.get(key).weight) + " \n")
            gml.write("    ] \n")
        gml.write( "] \n")


def readCSV(workList):
	fileCsv = 'data' + os.sep + 'report' + os.sep + 'gephi' + os.sep + 'report' + os.sep + 'analises.csv'
	analisesCSV = codecs.open(fileCsv, 'r', 'utf-8')
	text = analisesCSV.read()
	authorDict = countAuthors(workList)
	textCorrel = 'Autor;Numero Trabalho;Grau \n'
	textCorrelPR = 'Autor;Numero Trabalho;Page Rank \n'
	count = 0
	for line in text.split('\n'):
		if count > 0:
			lineArray = line.split(';')
			author = lineArray[0]
			grau = lineArray[2]
			pr = lineArray[9]
			textCorrel = textCorrel + author + ';' + str(authorDict.get(author)) + ';' + str(grau) + '\n'
			textCorrelPR = textCorrelPR + author + ';' + str(authorDict.get(author)) + ';' + str(pr) + '\n'
		count += 1

	folder = 'data' + os.sep + 'report'
	correlGrau = absFilePath('correlacaoGrau.csv', folder)
	with codecs.open(correlGrau, 'w', 'utf-8') as f:
	    f.write(textCorrel)

	correlPR = absFilePath('correlacaoPR.csv', folder)
	with codecs.open(correlPR, 'w', 'utf-8') as f:
	    f.write(textCorrelPR)


def addConections(graph):
	nodes1 = {}
	nodes2 = {}

	for key in graph.nodes:
		node = graph.nodes[key]
		if node.indegree > 9:
			nodes1[key] = node

	for key in graph.nodes:
		node = graph.nodes[key]
		if node.indegree < 3:
			nodes2[key] = node
	
	count = 0
	for key1 in nodes1:
		node = nodes1[key1]		
		for key2 in nodes2:
			#id1 = edgeIdGenerator(node, nodes2[key2])
			#id2 = edgeIdGenerator(nodes2[key2], node)
        	#if(graph.edges.get(id1) is None) and (graph.edges.get(id2) is None):
			loadEdge(graph.edges,node, nodes2[key2])
			#loadEdge(graph.edges,nodes2[key2],node)
			count = count + 1
	print count

	return graph





def main():
	jsonFilePath = sys.argv[1]
	jsonFile = codecs.open(jsonFilePath, 'r', 'utf-8')
	text = jsonFile.read()
	jsonData = json.loads(text)
	workJsonList = jsonData.get('Works')
	workList = []
	for w in workJsonList:
		downloadUrl = w.get('downloadUrl')
		id = w.get('id') 
		authorList = w.get('authorList')
		paperName = w.get('paperName')
		edicao = w.get('edicao')
		work = Work(id, authorList, paperName, edicao, downloadUrl)
		workList.append(work)
	#countWorkByEdicao(workList)
	#countAuthors(workList)
	#countAuthorsByEdicao(workList)
	#countWorkAloneByEdicao(workList)
	graph = buildGraph(workList)
	printGml(graph)
	graph = addConections(graph)
	printGml(graph, 'authorsColaborationGML2.gml')
	
	readCSV(workList)
		
	


if __name__ == '__main__':	
	main()