import sys
import time
from socket import *
import coloredlogs, logging
import subprocess
from contextlib import closing
from threading import Thread, Event
import struct
SOCKET_TIMEOUT = 10
import ecdsa
import sys, os
class SocketThread(Thread):
    clientSocket	= None
    kill_event 		= None
    logger 			= None

    def __init__(self, clientSocket, kill_event):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.g_kill_event = kill_event
        self.kill_event=Event()
        self.logger=logging.getLogger('__main__')

    def run(self):
        try:
            coloredlogs.install(level='INFO', logger=self.logger)
            self.clientSocket.settimeout(SOCKET_TIMEOUT)
            while not self.kill_event.is_set() and not self.g_kill_event.is_set():

                data = self.clientSocket.recv(2048)
                self.logger.debug(str(data))
                #self.logger.debug("data received: "+str(data))
                if len(data)>0:
                    req=chr(data[0])
                    response=b''
                    #logger.debug("Requested: "+req)
                    if(req=='g'):
                        try:
                            privKey, pubKey=ecdsa.generateKeyPair()
                            response=str(pubKey[0])+" "+str(pubKey[1])+":"+str(privKey)
                            response=response.encode()
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            logger.warning(exc_type, fname, exc_tb.tb_lineno)
                            response=b''
                    elif(req=='e'):
                        try:
                            buffLen=struct.unpack('i', data[1:1+4])[0]
                            keySize=struct.unpack('i', data[1+4:1+8])[0]
                            buff=data[1+8:1+8+buffLen]
                            privKey=int(data[1+8+buffLen:1+8+buffLen+keySize])
                            response=ecdsa.sign(buff, privKey)
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            logger.warning(exc_type, fname, exc_tb.tb_lineno)
                            response=b''
                    elif(req=='v'):
                        try:
                            buffLen=struct.unpack('i', data[1:1+4])[0]
                            sigLen=struct.unpack('i', data[1+4:1+8])[0]
                            buff=data[1+8:1+8+buffLen]
                            sig=data[1+8+buffLen:1+8+buffLen+sigLen]
                            pubKey=data[1+8+buffLen+sigLen:]
                            pubKey=[int(pubKey.split(b" ")[0]), int(pubKey.split(b" ")[1])]
                            if(ecdsa.verify(buff, sig, pubKey)):
                                response=struct.pack('i',1)
                            else:
                                response=struct.pack('i', 0)
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            logger.warning(exc_type, fname, exc_tb.tb_lineno)
                            response=struct.pack('i', 0)
                    self.clientSocket.send(response)
                else:
                    self.kill_event.set()
        except timeout:
            self.logger.warning('Timeout waiting data')
        except Exception as e:
            logger.exception(e)
        finally:
            self.kill_event.set()
            if self.clientSocket:
                self.clientSocket.close()
            self.logger.info('Closing')

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='INFO', logger=logger)

    server = None
    sockets = []
    global_kill_event = Event()

    logger.info('Crypto service started')
    with closing(socket(AF_INET, SOCK_STREAM)) as server:
        try:
            HOST = "0.0.0.0"
            PORT = 7777

            server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen()
            logger.info('Server listening on %s:%s' % (HOST, PORT))

            while True:
                logger.info('Waiting for new client')
                socketClient = SocketThread(server.accept()[0], global_kill_event)
                sockets.append(socketClient)
                socketClient.start()
        except Exception as e:
            logger.exception(e)
            logger.fatal('Terminating because error :(')
        except KeyboardInterrupt:
            global_kill_event.set()
            logger.info('CTRL+C pressed... terminating')
        finally:
            logger.info('Waiting for socket thread join')
            for socket in sockets:
                if socket:
                    logger.info('Socket %s closing' % socket)
                    socket.join()

            logger.info('Bye :)')
