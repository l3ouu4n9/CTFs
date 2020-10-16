#!/usr/bin/env python3

import requests
from base64 import b64encode, b64decode
import json
import uuid
import re
import math
import wave
import struct
import math
import time
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from math import sqrt


from multiprocessing import Pool

pool_size = 32
pool = Pool(pool_size)


import goertzelify

def decode_dtmf(name):
    # load wav file
    wav = wave.open(name, 'r')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    #print(wav.getparams())
    frames = wav.readframes(nframes * nchannels)
    # convert wave file to array of integers
    frames = struct.unpack_from("%dH" % nframes * nchannels, frames)
    # if stereo get left/right
    if nchannels == 2:
        left = [frames[i] for i in range(0,len(frames),2)]
        right = [frames[i] for i in range(1,len(frames),2)]
    else:
        left = frames
        right = left
    binsize = 800
    # Split the bin in 4 to average out errors due to noise
    binsize_split = 2
    
    indices = []
    for i in range(0,len(left)-binsize,binsize//binsize_split):
        indices.append((i, framerate, left, binsize))
    
    global goertzelify
    values = pool.map(goertzelify.goertzelify, indices)

    prevvalue = ""
    prevcounter = 0
    tmpres = []

    for value in values:
        if value==prevvalue:
            prevcounter+=1
            if prevcounter==1:
                tmpres += [value]
        else:
            prevcounter=0
            prevvalue=value

    res = []
    while len(tmpres) > 0:
        idx = tmpres.index(None)
        assert not idx == 0

        to_append = tmpres[:idx]
        rest = tmpres[idx + 1:]
        res.append(to_append)
        tmpres = rest
    for el in res:
        assert all([x == el[0] for x in el])
    return res

def decodeAudio(audio):
	content = b64decode(audio)
	f = open('file.bin', 'wb')
	f.write(content)
	f.close()
	decoded = decode_dtmf("file.bin")
	return decoded


keyboard = {
    '0' : '_0',
    '1' : '.,:1',
    '2' : 'abc2',
    '3' : 'def3',
    '4' : 'ghi4',
    '5' : 'jkl5',
    '6' : 'mno6',
    '7' : 'pqrs7',
    '8' : 'tuv8',
    '9' : 'wxyz9',
}

def decode_keyboard(keys_list):
    decoded = ''
    for keys in keys_list:
        c = keyboard[keys[0]][len(keys) - 1]
        decoded += c
    return decoded

def encode_keyboard(chars):
	s = ''
	for c in chars:
		for key in keyboard:
			if c in keyboard[key]:
				s += key * (keyboard[key].index(c) + 1)
	return s


def getMessage(session, url):
	for i in range(5):
		try:
			r = session.get(url)
			session.headers.update({"Authorization": "Bearer " + r.headers['newtoken']})
			return json.loads(r.text)
		except:
			print("FAILED REQUEST!!!!!!")
			time.sleep(1)

def sendMessage(session, url, message):
	for i in range(5):
		try:
			r = session.post(url, json = {'secretMessage': message})
			session.headers.update({"Authorization": "Bearer " + r.headers['newtoken']})
			return json.loads(r.text)
		except:
			print("FAILED REQUEST!!!!!!")
			time.sleep(1)

def greet(session, url, name):
	for i in range(5):
		try:
			r = session.post(url, json = {'name' : name})
			session.headers.update({"Authorization": "Bearer " + r.headers['newtoken']})
			return json.loads(r.text)
		except:
			print("FAILED REQUEST!!!!!!")
			time.sleep(1)

def check_flag(j):
	for key in j:
		if key not in ['message', 'secretMessage']:
			print(key, j[key])

def dist(d1, d2):
    def sqr(x):
        return x * x
    return int(math.sqrt(sqr(d1['x'] - d2['x']) + sqr(d1['y'] - d2['y']) + sqr(d1['z'] - d2['z']) + sqr(d1['t'] - d2['t'])))

def policz(cities):
    matrix = [[dist(cities[i], cities[j]) for i in range(128)] for j in range(128)]

    X = csr_matrix(matrix)
    Tcsr = minimum_spanning_tree(X)
    arr = Tcsr.toarray().astype(int)
    out = 0
    for row in arr:
        out += sum(row)
    return out


if __name__ == "__main__":
    intro_urls = { 'Romeo': 'http://codingbox5sh.reply.it:2449/romeo/introduce',
                   'Juliet': 'http://codingbox5sh.reply.it:2449/juliet/introduce'}

    urls = { 'Romeo' : 'http://codingbox5sh.reply.it:2449/romeo/private-channel',
             'Juliet': 'http://codingbox5sh.reply.it:2449/juliet/private-channel'}
    pattern_resp = re.compile('([\w])_of_the_city_(\d+)_is:_(\d+)')
    pattern_que = re.compile('what_is_the_([\w])_of_city_(\d+)')
    name = uuid.uuid4().hex
    s = requests.Session()

    person = 'Romeo'
    city = 0
    dim = 'x'
    cities = {}


    print('======INTRODUCING TO ROMEO=======')
    resp = greet(s, intro_urls[person], name)
    print('Romeo:', resp['message'])

    print('======ROMEO: GET ANSWER=======')
    response = getMessage(s, urls[person])
    secretMessage = decode_keyboard(decodeAudio(response['secretMessage']))
    print(f'Message from {person}:', response['message'])
    m_resp = pattern_resp.match(secretMessage)
    print(f'Answer from {person}: dim {m_resp.group(1)}, city {m_resp.group(2)}, value: {m_resp.group(3)}')
    if int(m_resp.group(2)) not in cities:
        cities[int(m_resp.group(2))] = {}
    cities[int(m_resp.group(2))][m_resp.group(1)] = int(m_resp.group(3))

    person = 'Juliet' if person == 'Romeo' else 'Romeo'


    while True:
        print(f'======{person}: GET QUESTION=======')
        response = getMessage(s, urls[person])
        check_flag(response)
        secretMessage = decode_keyboard(decodeAudio(response['secretMessage']))
        print(secretMessage)
        m_que = pattern_que.match(secretMessage)
        try:
            city = int(m_que.group(2))
            dim = m_que.group(1)
            print(f'Question from {person}: city {city}, dim {dim}')
            answer = encode_keyboard(str(cities[city][dim]))
        except:
            # how_long_is_the_shortest_trip_to_visit_all_cities
            answer = encode_keyboard(str(policz(cities)))
            print('FLAG:', secretMessage)
            print(cities)

        print(f'======{person}: POST ANSWER=======')
        print(f'Sending answer to {person}: {answer}')
        response = sendMessage(s, urls[person], answer)
        check_flag(response)
        secretMessage = decode_keyboard(decodeAudio(response['secretMessage']))
        print(secretMessage)
        print(f'Message from {person}:', response['message'])
        m_resp = pattern_resp.match(secretMessage)
        try:
            print(f'Answer from {person}: city {m_resp.group(2)}, dim {m_resp.group(1)}, value: {m_resp.group(3)}')
            if int(m_resp.group(2)) not in cities:
                cities[int(m_resp.group(2))] = {}
            cities[int(m_resp.group(2))][m_resp.group(1)] = int(m_resp.group(3))
        except:
            # those_are_all_the_cities_we_want_to_see
            print('WARN:', secretMessage)
            print(cities)


        person = 'Juliet' if person == 'Romeo' else 'Romeo'
