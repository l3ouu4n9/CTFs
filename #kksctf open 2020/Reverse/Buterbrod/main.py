import webview
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # _get_best_family,
from http import HTTPStatus
import threading
import time
from functools import partial
import os
import stage
import sys
import shutil
import urllib
import posixpath
import mimetypes
import struct
import zlib
import io


class SHRH_packed(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.initation()
        super().__init__(*args, **kwargs)

    def initation(self):
        self.protocol_version = stage.kek(b'wIq14S\rpd]Z9', b'7\r\xce\x16G\xd6\xd7\x00').decode()
        kek0 = stage.kek(b'eX&O5(pAbh=m', b'!M\x17\xf3\x9b\xd7o\xd4').decode()
        kek1 = stage.kek(b'|+rJ*j3?R:eP', b'H\x03y\xe6V\xed\xb1\xb5').decode()
        kek2 = stage.kek(b'|\t/KR?twE\n~{', b'O\x91R\xa0y>\x1a\xad').decode()
        kek3 = stage.kek(b'Sf6k>3C1E,Xy', b'\xd6\x9d\xf0T\xa3I\x90\x7f').decode()
        kek4 = stage.kek(b"A2h.X'tfC^(k", b']\xcb5\xff\x9a[\x8b|').decode()
        kek5 = stage.kek(b'qi!\x0b\tPo6E[Wl', b'Y\xfb}\x88V[\xddu').decode()
        self.files = {}
        with open(stage.kek(b'#:en\x0ciR\\W;-K', b'D\xed\x9d\xf6\xf5\xbf\x029').decode(), stage.kek(b'y:}J^UZOY*dS', b'\xb0E\x97\xbb\x17\x81\xf4\xba').decode()) as f:
            cnt = struct.unpack(kek5, f.read(4))[0]
            for i in range(cnt):
                data_len = struct.unpack(kek3, f.read(8))[0]
                name_len = struct.unpack(kek4, f.read(8))[0]
                name = zlib.decompress(f.read(name_len)).decode()
                data = zlib.decompress(f.read(data_len))
                self.files[name] = ({
                    kek0: name,
                    kek1: io.BytesIO(data),
                    kek2: len(data)
                })

    def do_GET(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.seek(io.SEEK_CUR, 0)
                # f.close()

    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.seek(io.SEEK_CUR, 0)
            # f.close()

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, stage.kek(b'u[f9@1s;aJi,', b')F\xcbG:\xcbe\x13h\x82\xc3\x04\x9f\x9dC\r').decode())
            return None
        try:
            f = self.files[path][stage.kek(b'^cSJx?|I-DiV', b'i\xb5e\xa0)i\x14\x84').decode()]
        except (OSError, KeyError):
            self.send_error(HTTPStatus.NOT_FOUND, stage.kek(b'u[f9@1s;aJi,', b')F\xcbG:\xcbe\x13h\x82\xc3\x04\x9f\x9dC\r').decode())
            return None

        try:
            self.send_response(HTTPStatus.OK)
            self.send_header(stage.kek(b'o"{\rwVjh6TuG', b'\x83\x17\xacz\x8c\x0c\xac\xc3\x90\xc1zDL\x93=D').decode(), self.guess_type(path))
            self.send_header(stage.kek(b'b`p_VwlyE/:f', b'cg\xa2\x93\xdcL\xcc\xdb]QL\x92\x12v\xea|').decode(),
                             self.files[path][stage.kek(b'pKq^!(m[9A*&', b'\xa4\xca\xc8Ueq\xc2\x02').decode()])
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def translate_path(self, path):
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Forget explicit trailing slash when normalizing. Issue17324
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = ""
        for word in words:
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': stage.kek(b"*W+\x0bJu#jFwz'", b"-2\x16\x9e\xdf|\xed\x9c\xd0\xfb\xe6Y\x8c\xd5(\x828j\xd3'\xebk\xcc\xa2").decode()
    })


class storage(object):
    # conceptual shit
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data


def do_srv(strg):
    print("Starting server")
    ServerClass = ThreadingHTTPServer
    addr = ("", 26883)
    with ServerClass(addr, SHRH_packed) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        try:
            strg.set_data(httpd)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
    print("Server started")


def callb(data):
    global w
    email, key = data.split(":")
    if not stage.stage(email, key):
        w.eval(stage.kek(b'Pjx_W"&\x0bC*:X', b'\xe6.\xe8\xe8l\x05\xd0\xf5t\xfe\xaf\xd0\xb3\xa3,.').decode())
    else:
        w.eval(stage.kek(b'Pi_e#RSCtFGm', b'1\xeb\x9f&\x0c\x91!\x00e\xccB\xf2\xf0\xef\xfa\xae"\xf6}A\x0f\xc2\xc5E').decode().format(email=email, key=key))


def initate_data_and_work():
    global w
    ev = threading.Event()
    strg_kek = storage()
    th = threading.Thread(target=do_srv, args=(strg_kek,))
    th.start()
    time.sleep(1)
    w = webview.WebView(width=550, height=750, title=stage.kek(b'T-R5:Eu32#=H', b'\xf2\x10\xcd\x80-\xc8\x84\x882k\xbc\xd8\xf2l\xa2\xc3').decode(),
                        url=stage.kek(b'?q6ACkSp<7Ix', b'\xe6C\x91\x0e\x13\xce\xdd\xd2VQ#W\x96H*O\xeb\xc0\xb7\x00>\xb9\x84\xd38oO\xafz~\xcdv\x04\x03>*\n4\xeb9').decode().format(26883, str(int(time.time()))), resizable=True, debug=True)
    w.bind(callb)
    time.sleep(0.1)
    try:
        while w.loop(True):
            pass
    finally:
        print(stage.kek(b' sO&3w,]J:z(', b'\x1by}\xf8\x0f\xd4x\xd1\xc7$\x9d\xdd\x80"\xba\xdd\xd1\x85)\xacc\xcfy\xb4S\xc9\x15\xf1-\x10\xb8\xf9').decode())
        strg_kek.get_data().shutdown()
        th.join()


if __name__ == "__main__":
    initate_data_and_work()
