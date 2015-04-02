# -*- coding: utf-8 -*-
import urllib2
from Model import *
from IOUtils import *



def readFile(filePath):	
	content = IOUtils.readFile(filePath)
	sbieEventList = []
	if content:
		countLine = 0
		for line in content.split('\n'):
			if line and countLine > 0:
				lineArray = line.split(';')
				url = lineArray[0]
				edicao = lineArray[1]
				sbieEvent = SbieEvent(url, edicao)				
				sbieEventList.append(sbieEvent)				
			countLine += 1
	return sbieEventList

def downloadEvent(sbieEventList):
	proxy = urllib2.ProxyHandler({'http': ''})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	folder = IOUtils.joinPaths('data', 'page2')
	for sbieEvent in sbieEventList:			
		try:
		    req = urllib2.Request(sbieEvent.url)
		    response = urllib2.urlopen(req)
		    html = response.read()		
		    fileParam = IOUtils.absFilePath(str(sbieEvent.edicao) + '.html' , folder)
		    IOUtils.saveFile(fileParam, html)    
		except:
		    print 'problem : ' + sbieEvent.url


def main():
	filePath = IOUtils.joinPaths('data', 'sbie.csv')
	sbieEventList = readFile(filePath)
	downloadEvent(sbieEventList)


if __name__ == '__main__':
    main()