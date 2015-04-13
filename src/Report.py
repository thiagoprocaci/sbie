# -*- coding: utf-8 -*-
import sys
import json
import codecs
import os
from IOUtils import *
from Graph import *


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
	fileParam = IOUtils.absFilePath('countWorkAloneByEdicao' , folder)
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
    fileParam = IOUtils.absFilePath('workCountByEdicao' , folder)
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
    fileParam = IOUtils.absFilePath('orderedAuthors' , folder)
    
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
	fileParam = IOUtils.absFilePath('authorsCountByEdicao' , folder)
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




def buildGraph(workList):
	nodeDict = {}
	edgeDict = {}
	for work in workList:
		for author in work.authorList:
			if author:
				nodeDict =  GraphSupport.loadNode(nodeDict, author, author)
	
	for work in workList:
		for author in work.authorList:
			for author2 in work.authorList:
				if author and author2:
					source = nodeDict.get(author)
					dest = nodeDict.get(author2)

					#print str(source) + ' ; ' + source.id
					GraphSupport.loadEdge(edgeDict, source, dest)
					GraphSupport.loadEdge(edgeDict, dest, source)
	graph = Graph(nodeDict, edgeDict)
	return graph

def printGml(graph, fileName = 'authorsColaborationGML.gml'):   
	
    nodes = graph.nodes
    edges = graph.edges
    folder = 'data' + os.sep + 'report'
    authorGML = IOUtils.absFilePath(fileName, folder)
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


# leitura das analises do gephi para gerar arquivo do excel
#funcao incompleta
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
	correlGrau = IOUtils.absFilePath('correlacaoGrau.csv', folder)
	with codecs.open(correlGrau, 'w', 'utf-8') as f:
	    f.write(textCorrel)

	correlPR = IOUtils.absFilePath('correlacaoPR.csv', folder)
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
			GraphSupport.loadEdge(graph.edges,node, nodes2[key2])
			#loadEdge(graph.edges,nodes2[key2],node)
			count = count + 1
	#print count

	return graph





def main():
	jsonFilePath = IOUtils.joinPaths('data','ICALT.json')
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
	countWorkByEdicao(workList)
	countAuthors(workList)
	countAuthorsByEdicao(workList)
	countWorkAloneByEdicao(workList)
	graph = buildGraph(workList)
	printGml(graph)
	graph = addConections(graph)
	printGml(graph, 'authorsColaborationGMLAddConnection.gml')
	
	#readCSV(workList)
		
	


if __name__ == '__main__':	
	main()