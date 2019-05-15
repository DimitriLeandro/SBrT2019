# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------------------------------
# SYS.ARGV[0] -> framesReader.py
# SYS.ARGV[1] -> pasta raiz do teste

# A pasta raiz do teste deve conter as pastas LOG, JSON e CSV, e dentro de JSON deve haver dois arquivos, frames.json e events.json

# EXEMPLO: dimi@dimi-lss01:~$ python3 framesReader.py ../../Aquisicoes/Pycom/Teste1
#------------------------------------------------------------------------------------------------------------------------------

import json
import sys
import os
from datetime import datetime

# PRIMEIRO EU VERIFICO SE OS PARÂMETROS SÃO VÁLIDOS
if len(sys.argv) != 2:
	print("Erro na entrada de parâmetros. 1 -> caminho para a pasta raiz da aquisicao.")
else:
	# LENDO OS PARÂMETROS
	arquivoJSON = sys.argv[1] + "/JSON/frames.json"

	# VERIFICANDO SE O ARQUIVO JSON EXISTE MESMO
	arquivoExiste = os.path.isfile(arquivoJSON)
	
	if arquivoExiste == False or arquivoExiste == 0:
		print("O arquivo JSON que você está tentando abrir não existe. Verifique o nome e o caminho.")
	else:
		# ABRINDO O ARQUIVO JSON E LENDO
		with open(arquivoJSON, 'r') as jsonFile:
			data = json.load(jsonFile)

		# CRIANDO UM ARQUIVO CSV PRA GRAVAR AS INFORMAÇÕES NELE TB
		nomeCSV = sys.argv[1] + "/CSV/GATEWAY_" + datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
		csvFile = open(nomeCSV, "a+")

		csvFile.write("fCnt,freq,bw,sf,cr,rssi,channel,timestamp" + "\n")
		
		# VOU PASSAR POR CADA ELEMENTO DO LORA E SALVAR APENAS O QUE EU QUERO
		for x in data:
			try:
				# VERIFICANDO SE É UM UPLINK
				if "uplinkFrame" in x["result"]:
					#VERIFICANDO SE NÃO É UM ACK
					ack 	= str(x["result"]["uplinkFrame"]["phyPayloadJSON"])
					jsonAck = json.loads(ack)
					ack 	= str(jsonAck["macPayload"]["fhdr"]["fCtrl"]["ack"])

					if ack == False or ack == "False":
						# SELECIONANDO APENAS OS DADOS QUE EU QUERO
						fCnt 	= str(x["result"]["uplinkFrame"]["phyPayloadJSON"])
						freq 	= str(x["result"]["uplinkFrame"]["txInfo"]["frequency"])
						bw		= str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["bandwidth"])
						sf 		= str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["spreadingFactor"])
						cr 		= str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["codeRate"])
						rssi 	= str(x["result"]["uplinkFrame"]["rxInfo"][0]["rssi"])
						channel = str(x["result"]["uplinkFrame"]["rxInfo"][0]["channel"])
						tStamp 	= str(x["result"]["uplinkFrame"]["rxInfo"][0]["timestamp"])						

						# O FRAME COUNT VEM DENTRO DE UMA STRING QUE NA VERDADE É UM JSON (IGAUL O ACK)
						jsonFrameCount = json.loads(fCnt)
						fCnt 	= str(jsonFrameCount["macPayload"]["fhdr"]["fCnt"])

						# PRINTANDO NO TERMINAL E ESCREVENDO NO CSV						
						stringFinal = fCnt + "," + freq + "," + bw + "," + sf + "," + cr + "," + rssi + "," + channel + "," + tStamp + "\n"
						csvFile.write(stringFinal)
			except:
				print("Algum dado não pôde ser lido")
		
		csvFile.close()