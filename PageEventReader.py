# -*- coding: utf-8 -*-
import sys
import codecs
import urllib2
import os

class SbieEvent:
	url = None
	edicao = None

	def __init__(self, url, edicao):
		self.url = url
		self.edicao = edicao

	def __str__(self):
		return str(self.edicao) + ' ' + str(self.url)


def absFilePath(fileName, folder):    
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder,fileName)
    return os.path.abspath(path)


def readFile(filePath):
	fileSbie = codecs.open(filePath, 'r')
	content = fileSbie.read()
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
	folder = 'data' + os.sep + 'pages'
	for sbieEvent in sbieEventList:			
		try:
		    req = urllib2.Request(sbieEvent.url)
		    response = urllib2.urlopen(req)
		    html = response.read()		
		    fileParam = absFilePath(str(sbieEvent.edicao) + '.html' , folder)
		    with codecs.open(fileParam, 'w') as f:
		        f.write(html)		    
		except:
		    print 'problem : ' + sbieEvent.url


def main():
	filePath = sys.argv[1]
	sbieEventList = readFile(filePath)
	downloadEvent(sbieEventList)


if __name__ == '__main__':
    main()