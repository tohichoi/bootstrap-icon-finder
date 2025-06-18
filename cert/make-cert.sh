#!/bin/bash
#

PRIVATE_KEY_FILE=biznas-private-key.pem
CSR_FILE=biznas.csr
CRT_FILE=biznas.crt

openssl genpkey -algorithm RSA -out $PRIVATE_KEY_FILE -aes256 || exit 1

openssl req -new -key $PRIVATE_KEY_FILE -out $CSR_FILE -config openssl-ip.conf || exit 1

openssl x509 -req -in $CSR_FILE -signkey $PRIVATE_KEY_FILE -out $CRT_FILE -days 3650 -extensions v3_req -extfile openssl-ip.conf  || exit 1

openssl x509 -in $CRT_FILE -noout -text || exit 1

python https_server.py -c config.toml &

curl --cacert $CRT_FILE "https://$1:$2"
# without check 
curl --insecure "https://$1:$2"
