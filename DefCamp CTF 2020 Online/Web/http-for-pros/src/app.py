from flask import Flask, request, render_template_string, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.args.get('content'):
        if 'application' in request.args.get('content'):
            return 'Try Harder! Blacklist #1'
        if 'popen' in request.args.get('content'):
            return 'Try Harder! Blacklist #2'
        if 'builtins' in request.args.get('content'):
            return 'Try Harder! Blacklist #3'
        if 'class' in request.args.get('content'):
            return 'Try Harder! Blacklist #4'
        if 'import' in request.args.get('content'):
            return 'Try Harder! Blacklist #5'
        if '__mro__' in request.args.get('content'):
            return 'Try Harder! Blacklist #6'
        if "\\x" in request.args.get('content'):
            return 'Try Harder! Blacklist #7' 
        if '_' in request.args.get('content'):
            return 'Try Harder! Blacklist #8'
        if 'flag' in request.args.get('content'):
            return 'Try Harder! Blacklist #9'
        if ' ' in request.args.get('content'):
            return 'Try Harder! Blacklist #10'    
        if 'X19jbGFzc19fDQo'.lower() in request.args.get('content').lower():
            return 'Try Harder! Blacklist #11'
        if 'Y2xhc3M'.lower() in request.args.get('content').lower():
            return 'Try Harder! Blacklist #12'
        if '#' in request.args.get('content'):
            return 'Try Harder! Blacklist #13'
        if '%' in request.args.get('content'):
            return 'Try Harder! Blacklist #14'
        if '\0' in request.args.get('content'):
            return 'Try Harder! Blacklist #15'
        if '\{g\}' in request.args.get('content'):
            return 'Try Harder! Blacklist #16'
        if '._' in request.args.get('content'):
            return 'Try Harder! Blacklist #17'
        if '.(' in request.args.get('content'):
            return 'Try Harder! Blacklist #18'
        if 'g(' in request.args.get('content'):
            return 'Try Harder! Blacklist #19'
        if '().' in request.args.get('content'):
            return 'Try Harder! Blacklist #20'
        if '_[.' in request.args.get('content'):
            return 'Try Harder! Blacklist #21'
        if '__' in request.url: 
            return 'Try Harder! Blacklist #22! You getting there ;)'
        if 'class' in request.url: 
            return 'Try Harder! Blacklist #23! You getting there ;)'

        return render_template_string(request.args.get('content'))
    else:
        return render_template('index.html')
    


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5000, threaded=True)