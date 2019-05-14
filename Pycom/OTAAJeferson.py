from network import LoRa
import socket
import ubinascii
import binascii
import struct
import machine
import time
import  uos
# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915, adr=True, tx_retries=0, device_class=LoRa.CLASS_A)
APP_EUI = '406d23713c2de17a'
APP_KEY = 'dae41ee5789b7cc4bdd10a0799df6a7d'

# remove default channels
for i in range(0, 72):
    lora.remove_channel(i)

# adding the Australian channels
print("add channels")
for i in range(0, 7):
    lora.add_channel(i, frequency=915200000 + i * 200000, dr_min=0, dr_max=3)
    lora.add_channel(65, frequency=917500000, dr_min=4, dr_max=4)

# create an OTA authentication params
app_eui = binascii.unhexlify(APP_EUI.replace(' ',''))
app_key = binascii.unhexlify(APP_KEY.replace(' ',''))

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print("attempt...")


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

count = 0
while True:

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    print(lora.frequency())
    # send some data

    count += 1
    send = str(count)
    print(count)

    s.send(send)

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)
