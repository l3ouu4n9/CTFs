#!/usr/bin/env python3

import subprocess

def sandbox(toexec):
    return subprocess.check_output(["sudo", "-u", "sandbox", "python3", "-c", toexec]).decode().strip()

try:
    code = input()[:100]
    for bad in ['#', '"""', "'''"]:
        code = code.replace(bad, "")
    assert code == code[::-1]
    exec(sandbox(code))
except:
    print(open(__file__,"r").read())