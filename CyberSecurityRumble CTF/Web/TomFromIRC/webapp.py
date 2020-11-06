from flask import redirect, Flask, render_template, request
from flask import url_for, send_from_directory, make_response

app = Flask(__name__)

SAVES = {}

@app.route('/', methods=["GET", "POST"])
def index():
    global SAVES
    if request.method == "POST":
        if len(SAVES) > 5000:
            SAVES = {}
        content = str(request.form["echo"])
        if request.args.get("save") is not None and request.content_length is not None and request.content_length < 666:
            SAVES[request.args.get("save")] = content
    else:
        content = "Nothing to echo"
    return render_template("index.html", msg=content)

@app.route('/debug/<id>', methods=["GET"])
def debug(id):
    try:
        return SAVES.pop(id, ":(")
    except:
        return ":("
     

if __name__ == '__main__':
    app.run()
