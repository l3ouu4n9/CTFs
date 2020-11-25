from datetime import datetime
import subprocess
import random
import socket
import _thread
import time
from contextlib import closing

class UDPServer:
    def __init__(self):
        self.host = '0.0.0.0'    # Host address
        self.port = 1024    # Host port
        self.sock = None    # Socket
        self.map={}
        self.logFile=open("/tmp/logs.txt", 'w+')
        self.usedPorts=[]
    def start_checker(self):
        _thread.start_new_thread(self.checker, ())
    def checker(self):
        while(True):
            try:
                toDel=[]
                for x in self.map.keys():
                    if('last' in self.map[x] and 'process' in self.map[x] and datetime.now().timestamp()-self.map[x]['last']>10):
                        self.printwt("Killing process "+str(self.map[x]['addr'])+" for inactivity!")
                        self.map[x]['process'].terminate()
                        toDel.append(self.map[x]['addr'])
                        toDel.append(x)
                for x in toDel:
                    del self.map[x]
                time.sleep(2)
            except Exception as ex:
                print(type(ex))
                print(ex)
    def find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
    def createNewProcess(self, addr, data):
        port=self.find_free_port()
        self.printwt('Launching new process, running on port '+str(port))
        process=subprocess.Popen(['./chall', '127.0.0.1', str(port), 'bot'])
        self.printwt("Binding "+str(addr)+" with "+str(('127.0.0.1', port))+ " and vice-versa!")
        self.map[addr]={}
        self.map[addr]['process']=process
        self.map[addr]['last']=datetime.now().timestamp()
        self.map[addr]['addr']=('127.0.0.1', port)
        self.map[addr]['loading']=True
        self.map[('127.0.0.1', port)]={}
        self.map[('127.0.0.1', port)]['addr']=addr
        self.map[('127.0.0.1', port)]['loading']=False
        time.sleep(5)
        self.map[addr]['loading']=False
        self.sock.sendto(data, ('127.0.0.1',port))
    def printwt(self, msg):
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')
    def configure_server(self):
        self.printwt('Creating socket...')
        self.printwt('Socket created')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt(f'Binding server to {self.host}:{self.port}...')
        self.sock.bind((self.host, self.port))
        self.printwt(f'Server binded to {self.host}:{self.port}')
    def forward(self, addr, data):
        if addr in self.map.keys():
            self.map[addr]['last']=datetime.now().timestamp()
            if(self.map[addr]['loading']==False):
                self.sock.sendto(data, self.map[addr]['addr'])
        elif addr[0]!="127.0.0.1":
            #Starting only if length equals login packet length
            if(len(data)!=36):
                return
            _thread.start_new_thread(self.createNewProcess,(addr,data,))
            return
    def handle_request(self, data, client_address):
        #self.printwt(f'[ REQUEST from {client_address} ]')
        self.forward(client_address, data)
    def wait_for_client(self):
        self.printwt('Waiting for clients...')
        while(True):
            try:
                data, client_address = self.sock.recvfrom(1024)
                self.handle_request(data, client_address)
            except OSError as err:
                self.printwt(err)
    def shutdown_server(self):
        self.printwt('Shutting down server...')
        self.sock.close()
server = UDPServer()

server.configure_server()
server.start_checker()
server.wait_for_client()
