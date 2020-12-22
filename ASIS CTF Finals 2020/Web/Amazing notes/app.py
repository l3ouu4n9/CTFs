from flask import *
import os
import re
import base64
import hashlib
import glob
import math
import json
import subprocess
import validators
import time
from shutil import rmtree
app = Flask(__name__)
secret_token = os.getenv("secret_token")
flag = os.getenv("flag")
app_addr = os.getenv("app_addr")
@app.after_request
def add_csp(r):
    r.headers["X-Frame-Options"] = "Deny"
    r.headers["Cache-Control"] = "no-store,no-cache"
    if(request.path != "/"):
        r.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'none'; frame-src 'none';"
    return r

def waf(ext):
    if(re.match("^\w{1,10}$",ext)):
        if(ext not in ["shtml","htm","html","mht","xsl","js","css"]):
            return True
    return False

def getip():
    ip = request.headers.get(os.getenv("real_ip_header"))
    if(ip == None):
        ip = request.remote_addr
    return hashlib.md5(ip.encode()).hexdigest()
def getdir():
    if(isadmin_()):
        return "./uploads/ADMIN%s"%getip()
    else:
        return "./uploads/%s"%getip()

def upload(ext,note):
    upload_dir = getdir()
    file_name = hashlib.md5(note.encode()).hexdigest()

    if(os.path.exists(upload_dir) == False):
        os.mkdir(upload_dir)
    file_path = "".join([upload_dir,"/",file_name,".",ext])

    note_file = open(file_path,"w+")
    note_file.write(note)
    note_file.close()

    return redirect(url_for("add_get",_scheme="https",_external=True))

def isadmin_():
    isadmin = False
    # admin has secret_token => samesite: None - secure - http only
    if("secret_token" in request.cookies and request.cookies["secret_token"] == secret_token):
        isadmin = True
    return isadmin

def chkip(ip):
    ip = hashlib.md5(ip.encode()).hexdigest()
    now = math.floor(time.time())
    filename = "./ip/%s" % ip

    if(os.path.isfile(filename)):
        rfile = open(filename,"r")
        lastrequest = int(rfile.read().strip())
        rfile.close()
    else:
        lastrequest = 0


    diff = now - lastrequest
    if(diff<60):
        return 60-diff
    else:
        wfile = open(filename,"w+")
        wfile.write(str(now))
        wfile.close()
        return "OK"
@app.route("/note/<note>",methods=["GET"])
def view_note(note):
    return send_from_directory(getdir(), filename=note, as_attachment=False)

@app.route("/",methods=["POST"])
def add_post():
    ext = request.form.get("ext")
    note = request.form.get("note")
    if(ext == None or note == None or len(note) > 0x200):
        abort(400)

    if(os.path.exists(getdir()) and len(glob.glob("%s/*" % getdir())) > 10 and isadmin_ == False):
        return "max 10 files for regular users"
    if(waf(ext)):
        return upload(ext,note)
    else:
        return "a hacker??? I'll report you to fbi"

@app.route("/flag",methods=["POST"])
def get_flag():
    isadmin = isadmin_()
    if("X-I-Want" not in request.headers):
        return json.dumps({"data":"What do you want?"}),{"Content-Type":"application/json"}
    
    wants = request.headers["X-I-Want"]
    if(wants == "joke"):
        return json.dumps({"data":" To understand what recursion is... You must first understand what recursion is"}),{"Content-Type":"application/json"}
    elif(wants == "flag" and isadmin == True):
        return json.dumps({"data":flag}),{"Content-Type":"application/json"}
    elif(wants == "flag" and isadmin == False):
        return json.dumps({"data":"What??? What is flag?"}),{"Content-Type":"application/json"}
    else:
        return json.dumps({"data":"what is that???"}),{"Content-Type":"application/json"}
    
@app.route("/delete_notes",methods=["GET"])
def remove_notes():
    if(os.path.exists(getdir()) == True and "ADMIN" not in getdir()):
        rmtree(getdir())
    return redirect(url_for("add_get",_scheme="https",_external=True))
    

@app.route("/notes_list.json",methods=["GET"])
def list_notes_json():
    return json.dumps([os.path.basename(x) for x in glob.glob("%s/*" % getdir())]),{"Content-Type" : "application/json;charset=utf-8"}

@app.route("/report",methods=["POST"])
def report():
    ip = getip()
    ck = chkip(ip)
    if(ck != "OK"):
        return "Too fast"
    url = request.form.get("url")
    if(url != None):
        valid = validators.url(url) and url[0:4] == "http"
        if(valid == True):
            subprocess.Popen(["python3","/usr/src/bot.py",base64.b64encode(url.encode()).decode()],cwd="/tmp")
            return "admin is comeinggggg"
        else:
            return "admin is not comeinggggg"
    else:
        return "URL?"

@app.route("/report",methods=["GET"])
def report_get():
    return """
<head>
    <title>Notes app</title>
</head>
<body>
    <h3><a href="/delete_notes">Delete Notes</a>&nbsp;&nbsp;&nbsp;<a href="/">Add Note</a>&nbsp;&nbsp;&nbsp;<a href="/report">Report</a></h3>
        <hr>
        <h3>Report us bad urls</h3>
        <form action="/report" method=POST>
        URL: 
        <input type="text" name="url" placeholder="url">
        <br>
        <input type="submit" value="submit">
        </form>
    <br>
</body>
    """

@app.route("/",methods=["GET"])
def add_get():
    return """
<head>
    <title>Amazing notes</title>
    <script src="/add.js"></script>
</head>
<body>
    <h3><a href="/delete_notes">Delete Notes</a>&nbsp;&nbsp;&nbsp;<a href="/">Add Note</a>&nbsp;&nbsp;&nbsp;<a href="/report">Report</a></h3>
        <hr>
        <h3> Add an amazing note </h3>
        <form action="/" id="noteform" method=POST>
        <input type="text" name="ext" value="txt" hidden>
        <textarea rows="11" cols="101" name="note" form="noteform" placeholder="Amazing content"></textarea>
        <br>
        <input type="submit" value="submit">
        </form>
        <b><div id="flag"></div></b>
        <br>
        <b>Notes: </b><br><br>
        <div id="notes">
        </div>
    <br>
</body>
"""

@app.route("/add.js",methods=["GET"])
def idx():
    return """
function addnote(filename){
    let div = document.createElement("div")
    let a = document.createElement("a");
    a.innerText = filename;
    a.href = `/note/${filename}`;
    div.appendChild(a);
    notes.appendChild(div);
}   

fetch("/flag",{"method":"POST","headers":{"X-I-Want":"flag"}}).then((r)=>{
    r.json().then((r)=>{
        flag.innerHTML = `FLAG: ${r.data}`;
    });
});

fetch("/notes_list.json").then((r)=>{
    r.json().then((r)=>{
        r.forEach(addnote);
    });
});
""",{"content-type":"application/javascript"}

