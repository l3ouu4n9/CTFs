import struct
import socket
import random

s = socket.socket()
port  = 1013
s.connect(('35.238.225.156',port))


coins = 100
health = 100
mana = 100
posx = 0
posy = 0
goblin = 0
terminated = 0
dummyflag = 0
vuln = random.randint(1,500)

while(1 == 1):
	print "Welcome to game"
	print "What would you like to do?"
	print "1. Speak to goblin in front of you(2 energy) \n 2. Move Forward 1 step(1 energy) \n 3. Move Backward 1 step(1 energy) \n 4. Move Left 1 step(1 energy) \n 5. Move Right 1 step(1 energy) \n 6. Exit "

	choice = input("Enter your choice : ")
	if choice == vuln:
		dummyflag = 1
	
	if choice == 1 :
		goblin = 1
	elif choice == 2 :
		posy = 1
	elif choice == 3 :
		posy = -1
	elif choice == 4 :
		posx = -1
	elif choice == 5 :
		posx = 1
	elif choice == 6 :
		terminated = 1

	packet = struct.pack("iiiiiiii",posx,posy,coins,health,mana,goblin,terminated,dummyflag)
	#print(packet)
	s.send(packet)
	print(s.recv(500*1024))
	if(terminated == 1):
		break;
	goblin = 0
	dummyflag = 0
	posx = 0
	posy = 0
