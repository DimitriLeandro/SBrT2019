#!/bin/bash

# PARAMETRO $0 -> curlFrames.sh
# PARAMETRO $1 -> jwt
# PARAMETRO $2 -> dev eui
# PARAMETRO $3 -> frames ou events
# PARAMETRO $4 -> caminho para onde salvar

rm -f "$4"

curl -sS --header "Accept: application/json" --header "Grpc-Metadata-Authorization: Bearer $1" "http://172.17.173.236:8080/api/devices/$2/$3" | sudo tee -a "$4"