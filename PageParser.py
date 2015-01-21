# -*- coding: utf-8 -*-
import sys
import codecs
import os
import re
import json
from bs4 import BeautifulSoup
from Model import *


def absFilePath(fileName, folder):    
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder,fileName)
    return os.path.abspath(path)


def findEdicao(path):
	pathArray = path.split(os.sep)
	fileName = pathArray[len(pathArray) - 1]
	pathArray = fileName.split('.')
	return pathArray[0]


def parseFiles(dir):	
	workList = []
	for f in os.listdir(dir):		
		path = os.path.join(dir,f)
		if os.path.isfile(path):
		    fileName = os.path.abspath(path)		    
		    edicao = findEdicao(path)
		    pagefile = codecs.open(fileName, 'r', encoding='utf-8')
		    html = pagefile.read()
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
	folder = 'data' + os.sep + 'worksMeta'
	fileParam = absFilePath('sbie.json' , folder)
	with codecs.open(fileParam, 'w', encoding='utf-8') as f:		
		f.write('{ "Works" : [ ')
		for idx, val in enumerate(workList):				
			f.write(val.toJson())
			if idx != len(workList) - 1:
				f.write(', ')
		f.write(' ] }')

def removeMultipleBlankSpace(string):
    return re.sub(' +',' ', string).strip()



def main():
	folderPath = sys.argv[1]
	workList = parseFiles(folderPath)
	saveAsJson(workList)
	


if __name__ == '__main__':	
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()