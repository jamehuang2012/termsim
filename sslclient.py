import socket
import ssl
import Constants
import requests
import datetime
import uuid
import json
import LoggerManager
import sessionmgr
import struct
import os
import Transaction
import Pack



def doTransaction():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    #print(Pack.packReuqest())
    with socket.create_connection((Constants.URL, Constants.PORT)) as sock:
        with context.wrap_socket(sock, server_hostname= Constants.URL) as ssock:
            #print(ssock.version())
            #print(ssock.cipher())
            #print(ssock.getpeercert())
            ssock.sendall(Pack.packReuqest())
            result = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
             
                result += data
                #log = LoggerManager.LoggerManager().logger
                #log.debug(result)

                Pack.parseRequest(result)

                break
    
            # Parse the response 


#doTransaction()

