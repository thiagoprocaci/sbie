# -*- coding: utf-8 -*-


class Work:
	id = None 
	authorList = None
	paperName = None
	edicao = None
	downloadUrl = None

	def __init__(self, authorList, paperName, edicao, downloadUrl):
		self.authorList = []
		for author in authorList:		
			author = author.replace('\t','')	
			author = author.replace('\r','')	
			author = author.replace('\n','')
			self.authorList.append(author)
		self.paperName = paperName.replace('"','')
		self.edicao = edicao
		self.downloadUrl = downloadUrl		
		urlArray = downloadUrl.split('/')
		lastIndex = len(urlArray) - 1
		self.id = str(urlArray[lastIndex - 1]) + '_' + str(urlArray[lastIndex])

	def toJson(self):
		json = '{ "id" : "' + str(self.id) + '" , \n'
		json = json + ' "paperName" : "' + self.paperName + '" , \n'
		json = json + ' "edicao" : ' + str(self.edicao) + ' , \n'
		json = json + ' "downloadUrl" : "' + str(self.downloadUrl) + '" , \n'
		json = json + ' "authorList" : [  \n'
		for idx, val in enumerate(self.authorList):
			json = json + ' "' + val + '" '
			if idx != len(self.authorList) - 1:
				json = json + ' ,'
		json = json + '] \n'
		json = json + '} \n'
		return json


class SbieEvent:
	url = None
	edicao = None

	def __init__(self, url, edicao):
		self.url = url
		self.edicao = edicao

	def __str__(self):
		return str(self.edicao) + ' ' + str(self.url)
