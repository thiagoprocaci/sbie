import sys
import json
import codecs
import os
import urllib2




def absFilePath(fileName, folder):    
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder,fileName)
    return os.path.abspath(path)



def main():
	jsonFilePath = sys.argv[1]
	jsonFile = codecs.open(jsonFilePath, 'r', 'utf-8')
	text = jsonFile.read()
	jsonData = json.loads(text)
	workList = jsonData.get('Works')
	folder = 'data' + os.sep + 'works'
	for work in workList:	
		ok = False
		while not ok:				
			try:
				url = work.get('downloadUrl')
				req = urllib2.Request(url)
				r = urllib2.urlopen(req)
				fileParam = absFilePath(work.get('id') + '.pdf', folder)
				with codecs.open(fileParam, 'wb') as f:
					f.write(r.read())
				ok = True
			except:
			    print 'problem : ' + work.get('downloadUrl')
			    ok = False
	


if __name__ == '__main__':	
	main()