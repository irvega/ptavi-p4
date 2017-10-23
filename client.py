#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import socket
import sys

if len(sys.argv) <4:
    sys.exit(' Use:python3 client.py ip port linea')
    
# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1] #string
PORT = sys.argv[2]
LINE = sys.argv[4:]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
#parametros:internet, IP, UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, int(PORT)))
    print("Enviando:", ' '.join(LINE))
    if sys.argv[3] == 'register':
        my_socket.send(bytes('REGISTER sip:'+' '.join(LINE)+' SIP/2.0\r\n\r\n',      'utf-8') + b'\r\n')
    #convierto para poder mandar - 2formas pasar bytes
        data = my_socket.recv(1024) #Se queda esperando si no llega
    print('Recibido -- ', data.decode('utf-8')) #vuelvo a convertir utf8

print("Socket terminado.")
