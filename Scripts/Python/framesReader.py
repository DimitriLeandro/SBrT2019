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

		csvFile.write("frequency,")
		csvFile.write("bandwidth,")
		csvFile.write("spreadingFactor,")
		csvFile.write("codeRate,")
		csvFile.write("timestamp,")
		csvFile.write("rssi,")
		csvFile.write("loraSnr,")
		csvFile.write("channel,")
		csvFile.write("rfChain,")
		csvFile.write("latitude,")
		csvFile.write("longitude,")
		csvFile.write("altitude,")
		csvFile.write("adr,")
		csvFile.write("adrAckReq,")
		csvFile.write("fCnt,")
		csvFile.write("fOpts\n")

		
		# VOU PASSAR POR CADA ELEMENTO DO LORA E SALVAR APENAS O QUE EU QUERO
		for x in data:
			try:
				# VERIFICANDO SE É UM UPLINK
				if "uplinkFrame" in x["result"]:
					#VERIFICANDO SE NÃO É UM ACK
					phyPayloadStr  = str(x["result"]["uplinkFrame"]["phyPayloadJSON"])
					phyPayloadJSON = json.loads(phyPayloadStr)					
					ack            = str(phyPayloadJSON["macPayload"]["fhdr"]["fCtrl"]["ack"])

					if ack == False or ack == "False":
						# SELECIONANDO A PRIMEIRA PARTE DOS DADOS
						frequency       = str(x["result"]["uplinkFrame"]["txInfo"]["frequency"])
						bandwidth       = str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["bandwidth"])
						spreadingFactor = str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["spreadingFactor"])
						codeRate        = str(x["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["codeRate"])
						timestamp       = str(x["result"]["uplinkFrame"]["rxInfo"][0]["timestamp"])
						rssi            = str(x["result"]["uplinkFrame"]["rxInfo"][0]["rssi"])
						loraSnr         = str(x["result"]["uplinkFrame"]["rxInfo"][0]["loraSnr"])
						channel         = str(x["result"]["uplinkFrame"]["rxInfo"][0]["channel"])
						rfChain         = str(x["result"]["uplinkFrame"]["rxInfo"][0]["rfChain"])
						latitude        = str(x["result"]["uplinkFrame"]["rxInfo"][0]["location"]["latitude"])
						longitude       = str(x["result"]["uplinkFrame"]["rxInfo"][0]["location"]["longitude"])
						altitude        = str(x["result"]["uplinkFrame"]["rxInfo"][0]["location"]["altitude"])
						
						# A SEGUNDA PARTE ESTÁ DENTRO DO PHYPAYLOADJSON
						adr             = str(phyPayloadJSON["macPayload"]["fhdr"]["fCtrl"]["adr"])
						adrAckReq       = str(phyPayloadJSON["macPayload"]["fhdr"]["fCtrl"]["adrAckReq"])
						fCnt            = str(phyPayloadJSON["macPayload"]["fhdr"]["fCnt"])
						fOpts           = str(phyPayloadJSON["macPayload"]["fhdr"]["fOpts"])

						# FORMATANDO O FOPTS, OU VEM NULL OU VEM OUTRO JSON, MAS EU QUERO BINÁRIO
						if(fOpts == "None"):
							fOpts = "False"
						else:
							fOpts = "True"

						# PRINTANDO NO TERMINAL E ESCREVENDO NO CSV						
						stringFinal = frequency + ","
						stringFinal = stringFinal + bandwidth + ","
						stringFinal = stringFinal + spreadingFactor + ","
						stringFinal = stringFinal + codeRate + ","
						stringFinal = stringFinal + timestamp + ","
						stringFinal = stringFinal + rssi + ","
						stringFinal = stringFinal + loraSnr + ","
						stringFinal = stringFinal + channel + ","
						stringFinal = stringFinal + rfChain + ","
						stringFinal = stringFinal + latitude + ","
						stringFinal = stringFinal + longitude + ","
						stringFinal = stringFinal + altitude + ","
						stringFinal = stringFinal + adr + ","
						stringFinal = stringFinal + adrAckReq + ","
						stringFinal = stringFinal + fCnt + ","
						stringFinal = stringFinal + fOpts + "\n"

						csvFile.write(stringFinal)
			except:
				print("framesReader.py -> Algum dado não pôde ser lido.")
		
		csvFile.close()