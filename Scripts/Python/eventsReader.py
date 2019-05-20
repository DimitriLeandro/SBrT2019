# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------------------------------
# SYS.ARGV[0] -> eventsReader.py
# SYS.ARGV[1] -> pasta raiz do teste

# A pasta raiz do teste deve conter as pastas LOG, JSON e CSV, e dentro de JSON deve haver dois arquivos, frames.json e events.json

# EXEMPLO: dimi@dimi-lss01:~$ python3 eventsReader.py ../../Aquisicoes/Pycom/Teste1
#------------------------------------------------------------------------------------------------------------------------------

import json
import sys
import os
from datetime import datetime
import base64

if len(sys.argv) != 2:
	print("Erro na entrada de parâmetros. 1 -> caminho para a pasta raiz da aquisicao. ")
else:
	# LENDO OS PARÂMETROS
	arquivoJSON = sys.argv[1] + "/JSON/events.json"

	# VERIFICANDO SE O ARQUIVO JSON EXISTE MESMO
	arquivoExiste = os.path.isfile(arquivoJSON)
	
	if arquivoExiste == False or arquivoExiste == 0:
		print("O arquivo JSON que você está tentando abrir não existe. Verifique o nome e o caminho.")
	else:
		# ABRINDO O ARQUIVO JSON E LENDO
		with open(arquivoJSON, 'r') as jsonFile:
			data = json.load(jsonFile)

		# CRIANDO UM ARQUIVO CSV PRA GRAVAR AS INFORMAÇÕES NELE TB
		nomeCSV = sys.argv[1] + "/CSV/ENDNODE_" + datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
		csvFile = open(nomeCSV, "a+")

		csvFile.write("fCnt,")
		csvFile.write("data,")
		csvFile.write("adr,")
		csvFile.write("dr,")
		csvFile.write("frequency\n")
		
		# VOU PASSAR POR CADA ELEMENTO DO LORA E SALVAR APENAS O QUE EU QUERO
		for x in data:
			try:
				# IGNORANDO OS ACKS
				if x["result"]["type"] == "uplink":
					# TODAS AS INFORMAÇÕES QUE EU QUERO ESTÃO DENTRO DE UMA STRING QUE É UM JSON
					stringPayLoad = str(x["result"]["payloadJSON"])
					jsonPayLoad   = json.loads(stringPayLoad)

					# PEGANDO AS INFORMAÇÕES
					fCnt      = str(jsonPayLoad["fCnt"])
					adr       = str(jsonPayLoad["adr"])					
					dr        = str(jsonPayLoad["txInfo"]["dr"])
					frequency = str(jsonPayLoad["txInfo"]["frequency"])					

					# PEGANDO A MENSAGEM QUE ESTA EM BASE64
					dataBase64 = str(jsonPayLoad["data"])
					data       = str(base64.b64decode(dataBase64))

					# REMOVENDO AQUELE b'' DA MENSAGEM
					data = data[2:-1]

					# PRINTANDO NO TERMINAL E ESCREVENDO NO CSV						
					stringFinal = fCnt + ","
					stringFinal = stringFinal + data + ","
					stringFinal = stringFinal + adr + ","				
					stringFinal = stringFinal + dr + ","
					stringFinal = stringFinal + frequency + "\n"

					# ESCREVENDO NO CSV
					csvFile.write(stringFinal)
			except:
				print("eventsReader.py -> Algum dado não pôde ser lido.")

		csvFile.close()