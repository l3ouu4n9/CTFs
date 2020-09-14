#!/usr/bin python
from Crypto.Util.number import *
import numpy as np
import random


def mess(msg):
	enc=""
	for i in msg:
		enc+=chr((ord(i)+ord(i))%256)
	return enc

	

def messig_up(message,key):
	parts=""
	while len(message)!=0:
		to_work_with=message[:9]
		first_one=np.zeros((3,3))
		k=0
		for i in range(3):
			for j in range(3):
				first_one[i][j]=ord(to_work_with[k])
				k+=1
		finish=np.transpose(np.matmul(first_one,key))
		for i in range(3):
			for j in range(3):
				parts=parts + str(finish[i,j])+ " "
		parts+="-----"
		message=message[9:]
	return parts



def recur_fibo(n): 
	if n<=1: 
		return 1
	else: 
		return recur_fibo(n-1)+recur_fibo(n-2)

def encode(n):
	i=1
	fib=recur_fibo(i)
	t_f=[]
	while fib<n:
		t_f.append(fib)
		i+=1
		fib=recur_fibo(i)
	_sum=0
	a_f=[]
	for i in range(len(t_f)-1,-1,-1):
		if _sum==n:
			break
		if _sum+t_f[i]<=n:
			a_f.append(t_f[i])
			_sum+=t_f[i]
	exis=[]
	for i in t_f:
		if i in a_f:
			exis.append(1)
		else:
			exis.append(0)
	return t_f,exis


def main():
	flag=open('flag.txt','r').read().strip()
	output=open('output.txt','w+')
	enc_flag=mess(flag)
	key=np.matrix("1 2 3;0 1 4;5 6 0")
	while len(enc_flag)%9!=0:
		enc_flag+='.'
	enc_flag=messig_up(enc_flag,key)
	arr=enc_flag.split('-----')
	for i in arr:
		g=i.split(' ')
		g=g[:-1]
		for j in g:
			output.write(str(encode(int(eval(j))))+'\n')

if __name__ == '__main__':
	main()
