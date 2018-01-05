#!/usr/bin/python
# -*- coding: utf-8 -*-
import textract
import re
import os
import sqlite3
import getmono

def getKeys(monolist, folder):
	
	conn = sqlite3.connect('database.db')
	cursor = conn.cursor()
	cursor.execute("create table teses( id INTEGER, titulo VARCHAR(255));")
	cursor.execute("create table chaves( id INTEGER, chave VARCHAR(255));")
	print "\nTabelas criadas no banco de dados"
	

	i = 0
	while (i < len(monolist)):
		
		
		if( "A&#771;" in monolist[i][1]):
			monolist[i][1] = monolist[i][1].replace('A&#771;', 'Ã')
			
			
		if( "O&#769;" in monolist[i][1]):
			monolist[i][1] = monolist[i][1].replace('O&#769;', 'Ó')
	
		cursor.execute("""
			insert into teses (id, titulo)
			values (?,?)
			""", (i, monolist[i][1].decode('utf-8')))		
		print "\n\n %s " %  monolist[i][1]

		count = 0
		dirname = os.path.join(folder, monolist[i][0])
		text = textract.process(dirname)
		text = text.replace('\n', '')

		expresion = re.compile(r'have[s]{0,1}: (.*?)\.')
		find = expresion.findall(text)
		if(find == []):
			print "\n Chave não encontrada"
			find = ["sem palavra-chave"]
		
		else:
			print "\n Chaves achadas\n"

		keys = find[0].split(",")


		j=0
		while (j < len(keys)):
			
			#Alguns ajustes estranhos que eu tive que fazer na mão 
			dict = {'ĂŁ':'ã', 'aĚ': 'ã', 'cĚ§': 'ç', 'ĂŞ': 'ê', 
			'Ă§': 'ç', 'ĂĄ': 'á', 'ĂŠ': 'é', 'Ă˘': 'â','IĚ': 'Í', 'oĚ': 'ó', 'uĂd': 'uíd' }
			
			for symbol, value in dict.items():
				if( symbol in keys[j]):
					keys[j] = keys[j].replace(symbol, value) 
	
			#Mais ajustes estranhos devido ao fato de algumas teses não terem o ponto final :s
			abstracts = ["viiiAbstract", "viiiABSTRACT", "viiABSTRACT", "xABSTRACT", "-6-ABSTRACT", "ABSTRACT"]
			for abstract in abstracts:
				if(abstract in keys[j]):
					keys[j] = keys[j][:keys[j].find(abstract)]
					
				
			#O que se tinha nesses casos dos parenteses que eu pulei era a tradução em inglês de uma palavra-chave, optei por tirar eles da jogada
			if(keys[j][0] == '(' or ( (keys[j][-1] == ')') and ('(' not in keys[j]) ) ):
				j+=1
				
			if('(' in keys[j] and ')' not in keys[j]):
				keys[j] = keys[j] + ')'
			
			cursor.execute("""
				insert into chaves (id, chave)
				values (?,?)
				""", (i, keys[j].decode('utf-8').lstrip()))
			print "\n + %s inserido em chaves" % keys[j].lstrip()
			conn.commit()

			j+=1
		i+=1

	conn.commit()
	conn.close()
	
if __name__ == "__main__":

	obj = getmono.GetMono("Engenharia+Eletrônica+e+de+Computação", 2017)
	lista = obj.monoList()
	getKeys(lista, "files/")

