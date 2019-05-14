#!/bin/bash

#------------------------------------------------------------------------------------------------------------------------------
# PARAMETRO $0 -> logToJson.sh
# PARAMETRO $1 -> pasta raiz do teste

# A pasta raiz do teste deve conter as pastas LOG, JSON e CSV, e dentro de LOG deve haver dois arquivos, frames.log e events.log

# EXEMPLO: dimi@dimi-lss01:~$./logToJson.sh ../../Aquisicoes/Pycom/Teste1
#------------------------------------------------------------------------------------------------------------------------------

# REMOVENDO OS ARQUIVOS DA PASTA JSON
rm -f "$1"/JSON/frames.json
rm -f "$1"/JSON/events.json

# COPIANDO OS ARQUIVOS DA PASTA LOG PARA A PASTA JSON
cp "$1"/LOG/frames.log "$1"/JSON/frames.json
cp "$1"/LOG/events.log "$1"/JSON/events.json

# ADICIONANDO UMA VIRGULA AO FINAL DE CADA LINHA
sed -i 's/$/,/' "$1"/JSON/frames.json
sed -i 's/$/,/' "$1"/JSON/events.json

# REMOVENDO A ULTIMA LINHA DOS ARQUIVOS 
sed -i '$d' "$1"/JSON/frames.json
sed -i '$d' "$1"/JSON/events.json

# ADICIONANDO COLCHETES NA PRIMEIRA LINHA
sed -i '1s/^/[\n/' "$1"/JSON/frames.json
sed -i '1s/^/[\n/' "$1"/JSON/events.json

# ANTES DE FECHAR O COLCHETES NA ULTIMA LINHA, EU TENHO QUE TIRAR A VIRGULA DA ULTIMA LINHA
sed -i '$ s/.$//' "$1"/JSON/frames.json
sed -i '$ s/.$//' "$1"/JSON/events.json

# ADICIONANDO COLCHETES NA ULTIMA LINHA
echo "]" >> "$1"/JSON/frames.json
echo "]" >> "$1"/JSON/events.json