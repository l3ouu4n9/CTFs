from flask import Flask, render_template, url_for, request, redirect
import urllib.request
from smb.SMBHandler import SMBHandler
import pwd, os
uid = pwd.getpwnam('ctfuser')[2]
os.setuid(uid)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
  return "Pirate Crawling and Storage System"

@app.route("/v1/", methods=["GET"])
def v1():
  return "V1 API ROUTE - disabled, see recent changelog"

@app.route("/v2/", methods=["GET"])
def v2():
  return "V2 API ROUTE"

@app.route("/v2/crawl", methods=["GET"])
def crawl():
  if request.args.get('adshua'):
    return urllib.request.urlopen(request.args.get('adshua')).read(100000)

@app.route("/v2/smb", methods=["GET"])
def smb():
  #this might ROCK YOUr world!
  if request.args.get('onlyifyouknowthesourcecode'):
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(request.args.get('onlyifyouknowthesourcecode'))
    buf = fh.read()
    fh.close()
    return buf

@app.route("/v2/CHANGELOG", methods=["GET"])
def changelog():
  return """
  #1: V1 context - V1 api routes disabled after sambacry
  #2: V2 context - crawl route parammeter changed to 'adshua' to prevent abuse
  #3: V2 context - added new safe SMbHandler to prevent sambacry
  """

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True, threaded=True)
