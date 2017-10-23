#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


PORT = int(sys.argv[1])
#datagram maneja UDP
class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    if len(sys.argv)<2:
        sys.exit(' Use:python3 server.py port')

    dic = {}
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print(self.client_address) #imprimir puerto e IP
        for line in self.rfile:
            if line:
                if line.decode('utf-8')[:8] == 'REGISTER':
                    print("El cliente nos manda:", line.decode('utf-8')) 
                    user = line.decode('utf-8')[13:-10]
                    self.dic[user] = self.client_address[0]
        print(self.dic)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    #Si lo dejo vacio es localhost, EchoH..manejador
    serv = socketserver.UDPServer(('', PORT), SIPRegistrerHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt: #cnt+C acabo programa
        print("Finalizado servidor")
