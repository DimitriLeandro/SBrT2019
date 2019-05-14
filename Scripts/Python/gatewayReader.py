# -*- coding: utf-8 -*-

import json
import sys
import os
from datetime import datetime

# EXEMPLO
# dimi@dimi-lss01:~$ python3 gatewayReader.py gateway.json 01422372

# PRIMEIRO EU VERIFICO SE OS PARÂMETROS SÃO VÁLIDOS
# SYS.ARGV[0] -> gatewayReader.py (SEMPRE VAI TER ESSE ARGUMENTO, VC SÓ VAI ESCREVER 2, MAS SEMPRE VÃO EXISTIR 3)
# SYS.ARGV[1] -> arquivoJsonQueEuQueroLer.json
# SYS.ARGV[2] -> id hexadecimal do endnode
if len(sys.argv) != 3:
	print("Erro na entrada de parâmetros. 1 -> caminho para o arquivo JSON. 2 -> id hexadecimal do end node desejado.")
else:
	# LENDO OS PARÂMETROS
	arquivoJSON = sys.argv[1]
	idEndNode 	= sys.argv[2]

	# VERIFICANDO SE O ARQUIVO JSON EXISTE MESMO
	arquivoExiste = os.path.isfile(arquivoJSON)
	
	if arquivoExiste == False or arquivoExiste == 0:
		print("O arquivo JSON que você está tentando abrir não existe. Verifique o nome e o caminho.")
	else:
		# ABRINDO O ARQUIVO JSON E LENDO
		with open(arquivoJSON, 'r') as jsonFile:
			data = json.load(jsonFile)

		# CRIANDO UM ARQUIVO CSV PRA GRAVAR AS INFORMAÇÕES NELE TB
		nomeCSV = "GATEWAY_" + datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
		csvFile = open(nomeCSV, "a+")

		csvFile.write("frame_count,rssi" + "\n")
		
		# VOU PASSAR POR CADA ELEMENTO DO LORA LIVE E SALVAR APENAS OS DADOS DO END NODE QUE EU QUERO
		for x in data:

			# VERIFICANDO SE A PARTE DO JSON QUE EU ESTOU TEM TUDO O QUE EU PRECISO (TEM ALGUNS QUE VEM SEM ESSE FHDR)
			try:
				if "fhdr" in x["phyPayload"]["macPayload"] and "uplinkMetaData" in x:

					# VERIFICANDO SE O ENDNODE ATUAL É O QUE ME INTERESSA
					if x["phyPayload"]["macPayload"]["fhdr"]["devAddr"] == idEndNode:

						# SELECIONANDO APENAS OS DADOS QUE EU QUERO
						frameCount = str(x["phyPayload"]["macPayload"]["fhdr"]["fCnt"])
						rssi = str(x["uplinkMetaData"]["rxInfo"][0]["rssi"])

						# PRINTANDO NO TERMINAL E ESCREVENDO NO CSV						
						stringFinal = frameCount + "," + rssi + "\n"
						csvFile.write(stringFinal)
			except:
				print("Algum dado não pôde ser lido")

		csvFile.close()