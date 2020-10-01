# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 2.7.17 (default, Apr 15 2020, 17:20:14) 
# [GCC 7.5.0]
# Warning: this version of Python has problems handling the Python 3 "byte" type in constants properly.

# Embedded file name: holdthepickle.py
# Compiled at: 2020-09-16 04:36:46
# Size of source mod 2**32: 975 bytes
import time, pickle

def dweeb(x):
    return int(bin(x)[2:])


def flagwrap():
    y = (
     dweeb(65), dweeb(115), dweeb(116), dweeb(114), dweeb(97), dweeb(102), dweeb(116), dweeb(119))
    return ('HAC{', y, '}')


def friends():
    print('Bonsoir')
    time.sleep(2)
    print('welcome to my challenge')
    time.sleep(2)
    print('I hope you like')
    time.sleep(2)
    user = input('Greetings....')
    if user == 'hi':
        print("hello! So simple to crack isn't it?")
        print("Here's your flag")
        print('HAC{lol}')
        return
    pickle_out = open('flag.pict', 'wb')
    pickle.dump(flagwrap(), pickle_out)
    pickle_out.close()
    print('Check the directory you copied this to ;)')
    extra = input('Anything else I can do for you?')
    if extra == 'y':
        input('What is it then?')
        print("sorry I can't do that, have you tried holding a pickle?")
    else:
        time.sleep(2)
        print("Okay, don't forget to hold the pickle.")


friends()
# okay decompiling holdthepickle.cpython-37.pyc
