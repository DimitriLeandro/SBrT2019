# -*- coding: utf-8 -*-

import os
import time
import sys
import base64

# EXEMPLO
# dimi@dimi-lss01:~$ python3 serverSender.py jwt dev_eui 10
# dimi@dimi-lss01:~$ python3 serverSender.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1zZXJ2ZXIiLCJleHAiOjE1NTc0OTcwNzMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NzQxMDY3Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYWRtaW4ifQ.bUqzV__aueIpv75vjxq-jr1YlZf1IfcQOFt7ljJFjb4 06348de5423ed1aa 1

# PRIMEIRO EU VERIFICO SE OS PARÂMETROS SÃO VÁLIDOS
# SYS.ARGV[0] -> serverSender.py (SEMPRE VAI TER ESSE ARGUMENTO, VC SÓ VAI ESCREVER 2, MAS SEMPRE VÃO EXISTIR 3)
# SYS.ARGV[1] -> jwt
# SYS.ARGV[2] -> dev_eui
# SYS.ARGV[3] -> tempo em segundos

if len(sys.argv) != 4:
	print("Erro na entrada de parâmetros. 1 -> JWT. 2 -> DEV_EUI.")
else:
	# LENDO OS PARÂMETROS
	jwt = sys.argv[1]
	dev_eui	= sys.argv[2]
	delay = sys.argv[3]

	contador = 0

	while(True):
		# ESCREVENDO A MENSAGEM QUE SERA ENVIADA
		mensagem = str(contador)
		mensagem = str(base64.b64encode(str.encode(mensagem)))
		mensagem = mensagem[2:-1]

		# CRIANDO A STRING DO COMANDO
		comando = "curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Grpc-Metadata-Authorization: Bearer " + str(jwt) + "' -d '{ "
		comando = comando + "\"deviceQueueItem\": {"
		comando = comando + "\"confirmed\": false, "
		comando = comando + "\"data\": \"" + mensagem + "\","
		comando = comando + "\"devEUI\": \"" + str(dev_eui) + "\","
		comando = comando + "\"fCnt\": 0,"
		comando = comando + "\"fPort\": 1 "
		comando = comando + "}"
		comando = comando + "}' 'http://172.17.173.236:8080/api/devices/" + str(dev_eui) + "/queue'"

		# EXECUTANDO O COMANDO
		os.system(comando)

		# DELAY E INCREMENTANDO CONTADOR
		contador += 1
		time.sleep(int(delay))
