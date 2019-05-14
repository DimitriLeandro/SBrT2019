#!/bin/bash

while :
do
	curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Grpc-Metadata-Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1zZXJ2ZXIiLCJleHAiOjE1NTc0OTcwNzMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NzQxMDY3Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYWRtaW4ifQ.bUqzV__aueIpv75vjxq-jr1YlZf1IfcQOFt7ljJFjb4' -d '{ 
	   "deviceQueueItem": {
	     "confirmed": true, 
	     "data": "ZWxlcyB0YW8gZGVpeGFuZG8gYSBnZW50ZSBzb25oYXI=",
	     "devEUI": "06348de5423ed1aa",
	     "fCnt": 0,
	     "fPort": 1 
	   }
	 }' 'http://172.17.173.236:8080/api/devices/06348de5423ed1aa/queue'

	sleep 1
done
