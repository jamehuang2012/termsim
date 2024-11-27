import socket
import ssl
from TransactionData import TransactionData
import Unpack
import LoggerManager
import Pack
from ParameterSingleton import ParameterSingleton


def doTransaction():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # check TransactionData.isRunning
    if TransactionData().isRunning == False:
        log = LoggerManager.LoggerManager().logger
        log.debug("Transaction stopped running")
        return
    
    p = ParameterSingleton()

    url = p.get_url()
    port = p.get_port()

    log = LoggerManager.LoggerManager().logger
    log.debug("URL: %s", url)
    log.debug("Port: %s", port)


    #print(Pack.packReuqest())
    with socket.create_connection((url, port)) as sock:
        with context.wrap_socket(sock, server_hostname= url) as ssock:
            #print(ssock.version())
            #print(ssock.cipher())
            #print(ssock.getpeercert())
            ssock.sendall(Pack.packReuqest())
            result = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    log = LoggerManager.LoggerManager().logger
                    log.debug("No data received")
                    break
             
                result += data
                log = LoggerManager.LoggerManager().logger
                log.debug(result)

                Unpack.parseResponse(result)

                break
    
            # Parse the response 


#doTransaction()

