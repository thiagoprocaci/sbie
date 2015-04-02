# -*- coding: utf-8 -*-
import sys
import json
from bs4 import BeautifulSoup
from Model import *
from IOUtils import * 



def findEdicao(path):
	pathArray = IOUtils.splitPath(path)
	fileName = pathArray[len(pathArray) - 1]
	pathArray = fileName.split('.')
	return pathArray[0]


def parseFiles(dir):	
	workList = []
	for f in IOUtils.listFiles(dir):		
		path = IOUtils.joinPaths(dir,f)
		if IOUtils.isFile(path):
		    fileName = IOUtils.absPath(path)		    
		    edicao = findEdicao(path)		    
		    html = IOUtils.readFile(fileName)
		    soup = BeautifulSoup(html)
		    tableList = soup.find_all('table', { "class" : "tocArticle" })        
		    for table in tableList:
				linkDownloadList = table.find_all('a', { "class" : "file" })		    	
				linkDownload = linkDownloadList[0]['href'].replace('view', 'download')
				authorsList = []
				tdAuthorsList = table.find_all('td', { "class" : "tocAuthors" })
				td = tdAuthorsList[0]			 		
				for a in td.getText().split(','):
					authorsList.append(a) 		
				tdPaper = table.find_all('td', { "class" : "tocTitle" })								
				td = tdPaper[0]				
				paper = td.getText()												
				if paper:											
					work = Work(authorsList, paper, edicao, linkDownload)						
					workList.append(work)					
	return workList
       
       
def saveAsJson(workList):
	fileParam = IOUtils.joinPaths('data','sbie.json')		
	with codecs.open(fileParam, 'w', encoding='utf-8') as f:		
		f.write('{ "Works" : [ ')
		for idx, val in enumerate(workList):				
			f.write(val.toJson())
			if idx != len(workList) - 1:
				f.write(', ')
		f.write(' ] }')
		

def main():	
	folderPath = IOUtils.joinPaths('data', 'pages')
	workList = parseFiles(folderPath)
	saveAsJson(workList)
	


if __name__ == '__main__':	
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()