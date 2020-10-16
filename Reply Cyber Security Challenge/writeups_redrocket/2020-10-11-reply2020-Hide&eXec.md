---
layout: post
category: coding
title: replyCTF 2020 - Hide & eXec
tags: 
    - hrshk
---

# Overview

We are given a zip file containing a barcode image and another zip file. To be able to extract from the inner zip file, we need the password first, which can be decoded from the barcode image. Obviously we need to automate the whole process. So I used python to do it for me. I used zxing library to decode the barcode.
When we decode the barcode we get some code in different programming languages each time. The languages used were, (bash, js, python, java, brainfuck, and php).
The next part was to detect the language. Then we can run the code with some language specific interpreter. (For Brainfuck I used, [https://github.com/fabianishere/brainfuck.git](https://github.com/fabianishere/brainfuck.git)).
We get the passcode and then do the same process over and over again to extract all the zip files. The script took 20-25 minutes to run on my machine and it will eventually spit out the flag in the end.

```python
import os
import subprocess
import zxing

reader = zxing.BarCodeReader()

def getfile():
    d = subprocess.check_output("ls")
    y = d.decode().split("\n")
    for i in y:
        if ".zip" in i:
            return i[:-4]

def uzip(fname, passcode):
    os.system(f"7z x {fname}.zip -p{passcode}")

def move(fname):
    os.system(f"mv {fname}.* move/")

def sol(fname):
    barcode = reader.decode(f"./{fname}.png")
    x = barcode.raw
    if ';' in x:
        code = x.replace("\n", "").replace(";", ";\n")
    else:
        code = x
    print(code)
    if "done;" in code:open(f"{fname}.sh", "w").write(code);passcode = subprocess.check_output(["bash", f"{fname}.sh"]).decode().strip()
    elif "var i" in code:open(f"{fname}.js", "w").write(code);passcode = subprocess.check_output(["node", f"{fname}.js"]).decode().strip() 
    elif "if i" in code or "zip(" in code:open(f"{fname}.py", "w").write(code);passcode = subprocess.check_output(["python", f"{fname}.py"]).decode().strip()
    elif "Main" in code:
        open(f"Main.java", "w").write(code)
        os.system("javac Main.java")
        passcode = subprocess.check_output(["java", "Main"]).decode().strip()
        os.system("mv Main.* move/")
    elif "++++" in code:
        open(f"{fname}.brainfuck", "w").write(code)
        passcode = subprocess.check_output(["./brainfuck", f"{fname}.brainfuck"]).decode().strip()
    elif "<?php" in code:
        open(f"{fname}.php", "w").write(code)
        passcode = subprocess.check_output(["php", f"{fname}.php"]).decode().strip()
    print(passcode)
    return passcode

if __name__ == '__main__':
	while True:
	    fname = getfile()
	    print(fname)
	    passcode = sol(fname)
	    uzip(fname, passcode)
	    move(fname)

	# {FLG:P33k-4-b0o!UF0undM3,Y0urT0olb0xIsGr8!!1}
```
