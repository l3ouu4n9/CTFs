# Victim bot
import os
import subprocess
import uuid
import LnkParse3 as Lnk
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    source = open(__file__, 'r').read().replace("\n", "\x3c\x62\x72\x3e").replace(" ", "\x26\x6e\x62\x73\x70\x3b")
    return source


@app.route('/send', methods=['POST'])
def sendFile():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    data = file.stream.read()
    if not data.startswith(b"\x4c\x00"):
        return "You're a bad guy!"
    shortcut = Lnk.lnk_file(indata=data)
    if shortcut.data['command_line_arguments'].count(" "):
        return "File is killed by antivirus."
    filename = str(uuid.uuid4())+".lnk"
    fullname = os.path.join(os.path.abspath(os.curdir) + "/uploads", filename)
    open(fullname, "wb").write(data)
    clickLnk(fullname)
    return "Clicked."


def clickLnk(lnkPath):
    subprocess.run('cmd /c "%s"' % lnkPath, capture_output=True, shell=True, check=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)