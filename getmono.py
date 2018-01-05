#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import urllib2
import os

#Engenharia+Eletrônica+e+de+Computação
class GetMono(object):
	def __init__(self, course, year):
		self.couser = course
		self.year = year
		self.link = "http://monografias.poli.ufrj.br/rel-pesquisacurso.php?fcurso=" + course
		self.data = requests.get(self.link).content
		self.limit = self.data.find("Ano: " + str(self.year-1))

	def generateDataArray(self):
		self.data = self.data[:self.limit]

		array = self.data.replace('\r\n', '').split("<br />")
		return array
	
	def monoList(self):
		expresionLink = re.compile(r'href="(.*?)"')
		expresionTitle = re.compile(r'"linkmonografia">(.*?)<')
		
		array = self.generateDataArray()
		
		i = 3
		list = []
		while (i < len(array)):
			#print i
			#print "\n"
			#print "http://monografias.poli.ufrj.br" + expresionLink.findall(array[i])[0][1:]
			#print expresionTitle.findall(array[i])[0]
			list.append([expresionLink.findall(array[i])[0][14:],
			expresionTitle.findall(array[i])[0]])
			i+=5
			
		return list
		
	def download(self):
		downloadList = self.monoList() 
		j = 0
		while (j < len(downloadList)):
			url = "http://monografias.poli.ufrj.br/monografias/" + downloadList[j][0] 
			filename = url.split('/')[-1]
			dirname = os.path.join('files/',filename)
			u = urllib2.urlopen(url)
			f = open(dirname, 'wb')
			meta = u.info()
			fileSize = int(meta.getheaders("Content-Length")[0])
			print "Downloading: %s Bytes: %s" % (filename, fileSize)

			downloadFileSize = 0
			blockSize = 8192
			while True:
				buffer = u.read(blockSize)
				if not buffer:
					break

				downloadFileSize += len(buffer)
				f.write(buffer)
				status = r"%10d  [%3.2f%%]" % (downloadFileSize, downloadFileSize * 100. / fileSize)
				status = status + chr(8)*(len(status)+1)
				print status,
			print "\n==> Downloaded \n"	
			f.close()
			j+=1


		
		
		
if __name__ == "__main__":
	
	obj = GetMono("Engenharia+Eletrônica+e+de+Computação", 2017)
	lista = obj.monoList()
	obj.download()
	
