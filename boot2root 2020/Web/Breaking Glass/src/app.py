from flask import Flask, request, redirect, url_for, render_template_string, render_template, jsonify, session, make_response, flash
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'insecurepassword'


def auth():
	token = request.cookies.get('token')
	if not token:
		session['logged_in'] = False
		return jsonify({'message': 'Missing token. Login again'}), 403
	try:
		data = jwt.decode(token, app.config['SECRET_KEY'])
		return data
	except:
		session['logged_in'] = False
		return jsonify({'message': 'Invalid token.Login again'}), 403

@app.route('/')
def index():
	if not session.get('logged_in'):
		res = make_response(render_template('index.html'))
		res.set_cookie('token', '', expires=0)
		session['logged_in'] = False
		return res;
	else:
		return redirect(url_for('user'))


@app.route('/login' ,methods = ['POST'])
def login():
	if request.method == 'POST' and request.form['nm'] == 'flask' and request.form['pass'] == 'password':
		session['logged_in'] = True
		token = jwt.encode({
			'user': request.form['nm'],
			'admin': False,
			'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
			},
			app.config['SECRET_KEY'])
		res = make_response(redirect(url_for('user')))
		res.set_cookie('token',token.decode('utf-8'))
		return res

	else:
		return make_response('Login Failed <a href="/">Try again</a>', 403,{'WWW-Authenticate':'Basic realm: "login Required"'})

@app.route('/user')
def user():
	data = auth()
	try:
		if data['admin']:
			return redirect(url_for('admin' , name = data['user']))
		if not data['admin']:
			return render_template('profile.html')
	except:
		return auth()

@app.route('/admin')
def admin():
	name = request.args.get('name') or None
	data = auth()
	try:
		if data['admin']:
			template = '''
			<!DOCTYPE html>
			<html>
			<head>
				<title>Admin profile</title>
			</head>
			<body>
				<div>
				<a class='logout' href="/logout">Logout</a>
				<div>
				<h1>Welcome! {} You have special powers.</h1>
			</div>
			</div>
			</body>
			</html>
			''' .format(name)
			return render_template_string(template)

		if not data['admin']:
			return render_template('profile,html')
	except:
		return auth()

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return redirect('/') 



if __name__ == '__main__':
	app.run(host='0.0.0.0')