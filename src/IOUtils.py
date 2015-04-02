# -*- coding: utf-8 -*-
import os
import codecs


class IOUtils:

	@staticmethod
	def getFileSeparator():
		return os.sep

	@staticmethod
	def splitPath(filePath):
		pathArray = filePath.split(os.sep)
		return pathArray

	@staticmethod	
	def absPath(filePath):
		return os.path.abspath(filePath)  

	@staticmethod	
	def absFilePath(fileName, folder):    
	    if not os.path.exists(folder):
	        os.makedirs(folder)
	    path = os.path.join(folder,fileName)
	    return os.path.abspath(path)

	@staticmethod
	def listFiles(folder):
		for f in os.listdir(folder):
			yield f

	@staticmethod
	def joinPaths(path1, path2):
		path = os.path.join(path1,path2)
		return path

	@staticmethod
	def isFile(path):
		return os.path.isfile(path)

	@staticmethod
	def saveFile(path, text):
		with codecs.open(path, 'w', encoding='utf-8') as f:
			f.write(text)

	@staticmethod
	def readFile(path):
		f = codecs.open(path, 'r', encoding='utf-8')
		text = f.read()
		return text
