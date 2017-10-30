#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import socket
import sys

if len(sys.argv) != 6:
    sys.exit(' Use:client.py ip puerto register sip_address expires_value')

SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINE = sys.argv[4]
EXPIRE = sys.argv[5]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    if sys.argv[3] == 'register':
        my_socket.send(bytes('REGISTER sip:' + LINE + ' SIP/2.0\r\nExpires: ' +
                             EXPIRE+'\r\n\r\n', 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))
print("Socket terminado.")
