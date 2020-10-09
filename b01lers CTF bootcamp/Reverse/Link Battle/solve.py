import ctypes

flag = ctypes.cdll.LoadLibrary('./libflaggen.so')
flag.getflag(0x1a0a)