# -*- coding: utf-8 -*-

import json
import sys
import os
from datetime import datetime
import base64

# EXEMPLO
# dimi@dimi-lss01:~$ python3 endNodeReader.py device.json

# PRIMEIRO EU VERIFICO SE OS PARÂMETROS SÃO VÁLIDOS
# SYS.ARGV[0] -> endNodeReader.py (SEMPRE VAI TER ESSE ARGUMENTO, VC SÓ VAI ESCREVER 1, MAS SEMPRE VÃO EXISTIR 2)
# SYS.ARGV[1] -> arquivoJsonQueEuQueroLer.json
if len(sys.argv) != 2:
	print("Erro na entrada de parâmetros. 1 -> caminho para o arquivo JSON. ")
else:
	# LENDO OS PARÂMETROS
	arquivoJSON = sys.argv[1]

	# VERIFICANDO SE O ARQUIVO JSON EXISTE MESMO
	arquivoExiste = os.path.isfile(arquivoJSON)
	
	if arquivoExiste == False or arquivoExiste == 0:
		print("O arquivo JSON que você está tentando abrir não existe. Verifique o nome e o caminho.")
	else:
		# ABRINDO O ARQUIVO JSON E LENDO
		with open(arquivoJSON, 'r') as jsonFile:
			data = json.load(jsonFile)

		# CRIANDO UM ARQUIVO CSV PRA GRAVAR AS INFORMAÇÕES NELE TB
		nomeCSV = "ENDNODE_" + datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
		csvFile = open(nomeCSV, "a+")

		csvFile.write("frame_count, rssi" + "\n")
		
		# VOU PASSAR POR CADA ELEMENTO DO JSON
		for x in data:
			try:
				# IGNORANDO OS ACK'S
				if str(x["type"]) == "uplink":
					dataBase64 = str(x["payload"]["data"])
					dataNormal = str(base64.b64decode(dataBase64))

					# REMOVENDO AQUELE b'' DA MENSAGEM
					dataNormal = dataNormal[2:]
					dataNormal = dataNormal[:-1]

					# PRINTANDO NO TERMINAL E ESCREVENDO NO CSV
					stringFinal = str(x["payload"]["fCnt"]) + "," + dataNormal + "\n"
					csvFile.write(stringFinal)
			except:
				print("Algum dado não pôde ser lido")

		csvFile.close()