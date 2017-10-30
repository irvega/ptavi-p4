#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
from time import gmtime, strftime, time
import json
import socketserver
import sys


PORT = int(sys.argv[1])
class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    if len(sys.argv)!=2:
        sys.exit(' Use:python3 server.py port')

    dic = {}
    def register2json(self):
        """
        Escribe en un fichero json
        """
        json.dump(self.dic, open('registered.json', 'w'))

    def json2registered(self):
        """
        Comprueba si hay fichero json
        """
        try:
            with open('registered.json', 'r') as file:
                self.dic = json.load(file)
                self.expiration()
        except(FileNotFoundError):
            pass

    def expiration (self):
        """
        Borra elementos expirados
        """
        expired = []
        time_exp = strftime('%Y-%m-%d %H:%M:%S',gmtime(time()))
        for user in self.dic:
            if self.dic[user][1] <= time_exp:
                expired.append(user)
        for user in expired:
            del self.dic[user]

    def handle(self): 
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        if self.dic == {}:
            self.json2registered()

        self.expiration()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print(self.client_address)
        for line in self.rfile:
            if line:
                if line.decode('utf-8')[:8] == 'REGISTER':
                    user = line.decode('utf-8')[13:-10]
                    ip = self.client_address[0]
                elif line.decode('utf-8')[:7] == 'Expires':
                    expires = int(line.decode('utf-8')[9:])+time()
                    expire = strftime('%Y-%m-%d %H:%M:%S', gmtime(expires))
                    if line.decode('utf-8').split(' ')[1][0] != '0':
                        self.dic[user] = [ip, expire]
                    else:
                        try:
                            del self.dic[user]
                        except(KeyError):
                            print('  NOTICE: This user dont exist!')
            print(line.decode('utf-8'),end='')
        print(self.dic)
        self.register2json()

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegistrerHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
