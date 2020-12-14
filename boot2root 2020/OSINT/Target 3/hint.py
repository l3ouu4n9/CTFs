import struct
import socket
import random

s = socket.socket()
port  = 1015
s.connect(('35.238.225.156',port))
print("This is a hint client only for finding the format of the date as a password for pastebin")
print("What number do you think corresponds to date here?")
packet = str(raw_input())
s.send(packet)
print(s.recv(80))
