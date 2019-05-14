from network import LoRa
import socket
import binascii
import struct
import time

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)

# create an OTA authentication params
dev_eui = binascii.unhexlify('4cecfdc2fd8dce2e')
app_eui = binascii.unhexlify('406d23713c2de17a')
app_key = binascii.unhexlify('d725df86100cdcc6b27a3276f5d1d7a4')

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('01422372'))[0]
nwk_swkey = binascii.unhexlify('3d8b2845476e82eceafec50c66e46c94')
app_swkey = binascii.unhexlify('624a041cbeda102fa3eed7817e7c753a')

# remove default channels
for i in range(0, 72):
    lora.remove_channel(i)

# adding the Australian channels
print("Adicionando canais Australianos...")
for i in range(0, 7):
    lora.add_channel(i, frequency=915200000 + i * 200000, dr_min=0, dr_max=5)
lora.add_channel(65, frequency=917500000, dr_min=4, dr_max=4)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# join a network using OTAA
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
join_wait = 0
while True:
    time.sleep(2.5)
    if not lora.has_joined():
        print('Tentando join...')
        join_wait += 1
        if join_wait == 5:
            print("Tente novamente.")
            lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
            join_wait = 0
    else:
        print("Join realizado!")
        break

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# variaveis que vou usar para enviar dados
msgEnviada = ""
rssi = 0

# ANTES DE TUDO, O DEVICE E QUEM INICIA A COMUNICACAO, PORTANTO, VOU ENVIAR A PRIMEIRA MENSAGEM
s.setblocking(True)
s.send("Inicio")
s.setblocking(False)
print("Iniciando a comunicacao...")

# LOOP DE ENVIO E RECEPCAO DE MENSAGENS
while(True):

    # RECEBENDO MENSAGEM
    msgRecebida = s.recv(64)

    if len(str(msgRecebida)) > 3:
        # SE CHEGAR ALGUMA COISA
        print("Resposta obtida!")
        rssi = lora.stats()[1] + 0
        msgEnviada = str(rssi)

        # RESPONDENDO
        s.setblocking(True)
        s.send(msgEnviada)
        s.setblocking(False)
        print("Enviando: " + msgEnviada)

    else:
        # SE NAO CHEGAR RESPOSTA
        s.setblocking(True)
        s.send("Sem resposta")
        s.setblocking(False)
        print("Enviando: Sem resposta")
