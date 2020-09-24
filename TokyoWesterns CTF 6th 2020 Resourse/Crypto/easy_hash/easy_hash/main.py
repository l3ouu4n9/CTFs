import struct
import os   

MSG = b'twctf: please give me the flag of 2020'

assert os.environ['FLAG']

def easy_hash(x):
    m = 0
    for i in range(len(x) - 3):
        m += struct.unpack('<I', x[i:i + 4])[0]
        m = m & 0xffffffff
    return m

def index(request):
    message = request.get_data()
    if message[0:7] != b'twctf: ' or message[-4:] != b'2020':
        return b'invalid message format: ' + message

    if message == MSG:
        return b'dont cheet'
    
    msg_hash = easy_hash(message)
    expected_hash = easy_hash(MSG)
    if msg_hash == expected_hash:
        return 'Congrats! The flag is ' + os.environ['FLAG']
    return 'Failed: easy_hash({}) is {}. but expected value is {}.'.format(message, msg_hash, expected_hash)
